from tornado.web import Application, RequestHandler


class App(Application):
    def __init__(self, app_handlers, app_settings):
        handlers = app_handlers.get()
        settings = app_settings.get()
        super().__init__(handlers=handlers, **settings)


class AppHandlers:
    def __init__(self, flags, log):
        opts = dict(flags=flags, log=log)
        self._handlers = [
            (r"/health", HealthHandler, opts),
        ]

    def get(self):
        return self._handlers


class AppSettings:
    def __init__(self, log, flags):
        self._log = log.bind(is_request_log=True, is_app_log=False)
        self._settings = dict(debug=flags["debug"], log_function=self._log_function)

    def get(self):
        return self._settings

    def _log_function(self, handler):
        if handler.get_status() < 400:
            log_method = self._log.info
        elif handler.get_status() < 500:
            log_method = self._log.warning
        else:
            log_method = self._log.error

        request_time = 1000.0 * handler.request.request_time()

        log_method(
            handler._request_summary(),  # pylint: disable=protected-access
            req_status=handler.get_status(),
            req_time=request_time,
        )


class ExceptionHandler:
    def log_exception(
        self, exc_type, exc_info, trace_back
    ):  # pylint: disable=unused-argument
        if getattr(self, "_logger"):
            self._logger.error(  # pylint: disable=no-member
                "Request: Error", exc_info=exc_info, stack_info=True
            )


class HealthHandler(ExceptionHandler, RequestHandler):
    def initialize(self, flags, log):  # pylint: disable=unused-argument
        self._logger = log  # pylint: disable=attribute-defined-outside-init

    def data_received(self, chunk):
        pass

    def get(self):
        self.write({"healthy": True})
        self.flush()
