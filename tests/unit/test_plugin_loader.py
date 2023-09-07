import pytest
from unittest.mock import patch

from bugjira.exceptions import PluginLoaderException
from bugjira.plugin_loader import load_plugin


def test_load_plugin_with_none_config():
    """
    GIVEN the load_plugin method from bugjira.plugin_loader
    WHEN we call it with config=None
    THEN a PluginLoaderException is raised
    """
    with pytest.raises(PluginLoaderException):
        load_plugin(config=None)


def test_load_plugin_with_good_config(good_config_dict):
    """
    GIVEN the load_plugin method from bugjira.plugin_loader
    WHEN we call it with a good config file
    THEN the bugjira.json_generator.register method should be called once
    """
    with patch("bugjira.json_generator.JsonGenerator.register") as register:
        load_plugin(good_config_dict)
        assert register.call_count == 1


def test_load_plugin_with_empty_config(good_config_dict):
    """
    GIVEN the load_plugin method from bugjira.plugin_loader
    WHEN we call it with config={}
    THEN the bugjira.json_generator.register method should be called once
    """
    with patch("bugjira.json_generator.JsonGenerator.register") as register:
        load_plugin({})
        assert register.call_count == 1


def test_load_plugin_with_bad_module_name(good_config_dict):
    """
    GIVEN the load_plugin method from bugjira.plugin_loader
    WHEN we call it with a config where the value for "json_generator_module"
        is the name of a non-existent module
    THEN a PluginLoaderException should be raised with the correct message
    """
    good_config_dict["json_generator_module"] = "foo.bar.nexiste.pas"
    with pytest.raises(PluginLoaderException,
                       match="Could not load module"):
        load_plugin(good_config_dict)
