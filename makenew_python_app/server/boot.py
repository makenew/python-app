from os import environ, path

from .server import Server
from .config import configure


def boot(create_dependencies):
    config_path = environ.get("PYAPP_CONFIG_PATH") or path.realpath(
        path.join(path.dirname(__file__), "..", "..", "config")
    )
    server = Server(create_dependencies, config_path)
    server.update_config_factory(configure)
    server.run()
