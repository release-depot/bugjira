import importlib

from bugjira.exceptions import PluginLoaderException


def import_module(name):
    """Use importlib.import_module to import a plugin class

    :param name: The fully qualified module name to import
    :type name: str
    :return: The module returned from the importlib.import_module method
    :rtype: module
    """
    return importlib.import_module(name)


def load_plugin(config={}):
    """Load a plugin using configuration in the supplied config dict. An empty
    config will result in loading the default json_generator module.

    :param config: A Bugjira config dict, defaults to {}. Cannot be None.
    :type config: dict, optional
    """

    if config is None:
        raise PluginLoaderException("cannot load plugin with config=None")

    # default to the bugjira-supplied default json_generator module
    module_name = config.get("json_generator_module",
                             "bugjira.json_generator")
    try:
        imported_module = import_module(module_name)
        plugin = imported_module.get_generator()
    except ModuleNotFoundError:
        raise PluginLoaderException(
            f"Could not load module named '{module_name}'"
        )
    plugin.register(config=config)
