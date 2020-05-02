from pinject import BindingSpec, new_object_graph, copy_args_to_public_fields

from .app import App, AppHandlers, AppSettings
from .lifecycle import Lifecycle


def create_dependencies(config, log):
    flags = {"debug": config.get("debug")}

    class FlagsBindingSpec(BindingSpec):
        def configure(self, bind):
            bind("flags", to_instance=flags)

    class LogBindingSpec(BindingSpec):
        def configure(self, bind):
            bind("log", to_instance=log)

    binding_specs = [FlagsBindingSpec(), LogBindingSpec()]

    classes = [
        App,
        AppHandlers,
        AppSettings,
        Lifecycle,
    ]

    obj_graph = new_object_graph(
        modules=None, classes=classes, binding_specs=binding_specs
    )

    return obj_graph.provide(Dependencies)


class Dependencies:
    @copy_args_to_public_fields
    def __init__(self, app, lifecycle, log):
        pass
