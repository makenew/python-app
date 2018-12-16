from tornado.web import Application, RequestHandler

class App(Application):
    def __init__(self, log, app_handlers, app_settings):
        handlers = app_handlers.get()
        settings = app_settings.get()
        super().__init__(handlers=app_handlers.get(), **settings)

class AppHandlers():
    def __init__(self):
        self.__handlers = [
            (r"/health", HealthHandler),
        ]

    def get(self):
        return self.__handlers

class AppSettings():
    def __init__(self, log, flags):
        self.__log = log
        self.__settings = dict(
            debug=flags,
            log_function=self.__log_function
        )

    def get(self):
        return self.__settings

    def __log_function(self, handler):
        if handler.get_status() < 400:
            log_method = self.__log.info
        elif handler.get_status() < 500:
            log_method = self.__log.warning
        else:
            log_method = self.__log.error

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
