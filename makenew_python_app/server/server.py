import logging
import sys
import asyncio
import signal
import time
from functools import partial

import rapidjson
from humps import camelize
import structlog
from structlog import get_logger
from tornado import ioloop, httpserver
from tornado.options import define, options


class Server:
    def __init__(self, create_dependencies, config_path):
        self._config_factory = ConfigFactory(config_path)
        self._create_dependencies = create_dependencies

    def run(self):
        config = self._get_config()
        log = create_logger(config.get("env") == "production", config.get("log"))
        dependencies = self._create_dependencies(config, log)

        lifecycle_log = log.bind(is_lifecycle_log=True, is_app_log=False)

        app = dependencies.app
        log = dependencies.log
        lifecycle = dependencies.lifecycle

        create_server(config, app, lifecycle_log)

        lifecycle_log.info("Initialize: Start")
        lifecycle_log.info(f"Server: http://localhost:{options.port}")
        io_loop = ioloop.IOLoop.instance()

        try:
            lifecycle.on_start()
        except BaseException as err:  # pylint: disable=broad-except
            lifecycle_log.critical("On Start: Fail", exc_info=err, stack_info=True)
            sys.exit(2)

        io_loop.start()
        lifecycle_log.info("Startup: Success")

    def update_config_factory(self, configure):
        self._config_factory = configure(self._config_factory)

    def _get_config(self):
        return self._config_factory.create()


class ConfigFactory:
    def __init__(self, config_path):  # pylint: disable=unused-argument
        self._config = {}

    def update(self, key, value):
        self._config[key] = value

    def create(self):
        return self._config


def create_logger(is_prod, log_config):
    def log_serializer(data, **kw_args):  # pylint: disable=unused-argument
        if log_config.get("camelize"):
            return rapidjson.dumps(camelize(data))
        return rapidjson.dumps(data)

    processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ]

    if is_prod:
        processors = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_log_level_number,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.TimeStamper(utc=True, key="time"),
            structlog.processors.JSONRenderer(serializer=log_serializer),
        ]

    logging.basicConfig(format="%(message)s", level=log_config.get("level").upper())

    structlog.configure(
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
        processors=processors,
    )

    log = get_logger()
    log_props = get_log_props(is_prod, log_config)
    return log.bind(**log_props)


def get_log_props(is_prod, log_config):
    if not is_prod:
        return {}
    return {
        "@service": log_config.get("service"),
        "@system": log_config.get("system"),
        "@env": log_config.get("env"),
        "name": log_config.get("name"),
        "version": log_config.get("version"),
        "is_app_log": True,
    }


def create_server(config, app, log):
    default_port = config.get("port")
    default_shutdown_delay = config.get("shutdown_delay")
    default_debug = config.get("env") == "development"

    define("port", default=default_port, help="run on the given port", type=int)
    define(
        "shutdown_delay",
        default=default_shutdown_delay,
        help="time to wait for shutdown",
        type=int,
    )
    define("debug", default=default_debug, help="run in debug mode", type=int)

    server = httpserver.HTTPServer(app)
    server.listen(options.port)

    signal.signal(signal.SIGTERM, partial(handle_signal, server, log))
    signal.signal(signal.SIGINT, partial(handle_signal, server, log))

    return server


def handle_signal(server, log, sig, frame):  # pylint: disable=unused-argument
    log.info("Signal: Interrupt")

    io_loop = ioloop.IOLoop.instance()

    def stop_loop(server, deadline):
        now = time.time()

        tasks = [
            t
            for t in asyncio.all_tasks()
            if t is not asyncio.current_task() and not t.done()
        ]

        if now < deadline and len(tasks) > 0:
            log.info("Shutdown: Wait", pending_tasks=len(tasks))
            io_loop.add_timeout(now + 1, stop_loop, server, deadline)
            return

        pending_connection = len(
            server._connections  # pylint: disable=protected-access
        )
        if now < deadline and pending_connection > 0:
            log.info("Shutdown: Wait", connections=pending_connection)
            io_loop.add_timeout(now + 1, stop_loop, server, deadline)
        else:
            log.info("Server: Close", connections=pending_connection)
            io_loop.stop()
            log.info("Shutdown: Success")

    def shutdown():
        try:
            log.info("Shutdown: Start", delay=options.shutdown_delay)
            deadline = time.time() + options.shutdown_delay
            stop_loop(server, deadline)
        except BaseException as err:  # pylint: disable=broad-except
            log.critical("Shutdown: Fail", exc_info=err, stack_info=True)
            sys.exit(1)

    io_loop.add_callback_from_signal(shutdown)
