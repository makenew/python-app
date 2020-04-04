from tornado.web import Application, RequestHandler

class App(Application):
    def __init__(self, log, app_handlers, app_settings):
        handlers = app_handlers.get()
        settings = app_settings.get()
        super().__init__(handlers=app_handlers.get(), **settings)

class AppHandlers():
    def __init__(self):
        self._handlers = [
            (r"/health", HealthHandler),
        ]

    def get(self):
        return self._handlers

class AppSettings():
    def __init__(self, log, flags):
        self._log = log
        self._settings = dict(
            debug=flags,
            log_function=self._log_function
        )

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
            handler._request_summary(),
            req_status=handler.get_status(),
            req_time=request_time,
        )

class HealthHandler(RequestHandler):
    def get(self):
        self.write({'healthy': True})
        self.flush()
