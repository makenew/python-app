from os import environ


def configure(config_factory):
    log_config(config_factory)
    server_config(config_factory)
    app_config(config_factory)
    return config_factory


def server_config(config_factory):
    env = environ.get("PYAPP_ENV") or "development"
    is_dev = env == "development"
    config_factory.update("env", env)
    config_factory.update("debug", environ.get("PYAPP_DEBUG") or is_dev)
    config_factory.update("port", environ.get("PORT") or 9000)
    config_factory.update("shutdown_delay", environ.get("PYAPP_SHUTDOWN_DELAY") or 3)


def app_config(config_factory):  # pylint: disable=unused-argument
    pass


def log_config(config_factory):
    config = {
        "camelize": environ.get("LOG_CAMELIZE") == "true",
        "level": environ.get("LOG_LEVEL") or "info",
        "service": environ.get("LOG_SERVICE"),
        "system": environ.get("LOG_SYSTEM"),
        "env": environ.get("LOG_ENV"),
        "name": environ.get("LOG_NAME"),
        "version": environ.get("LOG_VERSION"),
    }
    config_factory.update("log", config)
