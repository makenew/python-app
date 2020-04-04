from sys import exit
import asyncio
import signal
import time
from functools import partial

import structlog
from structlog import get_logger
from tornado import ioloop, httpserver
from tornado.options import define, options

class Server():
    def __init__(self, create_dependencies, config_path):
        self._config_factory = ConfigFactory(config_path)
        self._create_dependencies = create_dependencies

    def run(self):
        config = self._get_config()
        log = create_logger(config.get('env') == 'production')
        dependencies = self._create_dependencies(config, log)

        app = dependencies.app
        log = dependencies.log

        server = create_server(config, app, log)

        log.info('Initialize: Start')
        log.info(f'Server: http://localhost:{options.port}')
        log.info('Startup: Success')
        ioloop.IOLoop.instance().start()

    def update_config_factory(self, configure):
        self._config_factory = configure(self._config_factory)

    def _get_config(self):
        return self._config_factory.create()

class ConfigFactory():
    def __init__(self, config_path):
        self._config = {}
        pass

    def update(self, key, value):
        self._config[key] = value

    def create(self):
        return self._config

def create_logger(is_prod):
    if (is_prod):
        structlog.configure(processors=[structlog.processors.JSONRenderer()])

    log = get_logger()
    return log

def create_server(config, app, log):
    default_port = config.get('port')
    default_shutdown_delay = config.get('shutdown_delay')
    default_debug = config.get('env') == 'development'

    define("port", default=default_port, help="run on the given port", type=int)
    define("shutdown_delay", default=default_shutdown_delay, help="time to wait for shutdown", type=int)
    define("debug", default=default_debug, help="run in debug mode", type=int)

    server = httpserver.HTTPServer(app)
    server.listen(options.port)

    signal.signal(signal.SIGTERM, partial(handle_signal, server, log))
    signal.signal(signal.SIGINT, partial(handle_signal, server, log))

    return server

def handle_signal(server, log, sig, frame):
    log.info('Signal: Interrupt')

    io_loop = ioloop.IOLoop.instance()

    def stop_loop(server, deadline):
        now = time.time()

        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()]

        if now < deadline and len(tasks) > 0:
            log.info('Shutdown: Wait', pending_tasks=len(tasks))
            io_loop.add_timeout(now + 1, stop_loop, server, deadline)
            return

        pending_connection = len(server._connections)
        if now < deadline and pending_connection > 0:
            log.info('Shutdown: Wait', connections=pending_connection)
            io_loop.add_timeout(now + 1, stop_loop, server, deadline)
        else:
            log.info('Server: Close', connections=pending_connection)
            io_loop.stop()
            log.info('Shutdown: Success')

    def shutdown():
        try:
            log.info('Shutdown: Start', delay=options.shutdown_delay)
            deadline = time.time() + options.shutdown_delay
            stop_loop(server, deadline)
        except BaseException as e:
            log.error(e)
            exit(1)

    io_loop.add_callback_from_signal(shutdown)
