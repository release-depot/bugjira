import pytest
from unittest.mock import patch, mock_open

from bugjira import json_generator
from bugjira.exceptions import JsonGeneratorException
from bugjira.json_generator import JsonGenerator

EXPECTED_BZ_FIELD_COUNT = 3
EXPECTED_JIRA_FIELD_COUNT = 2


def test_init_good_config(good_config_dict, good_sample_fields_file_path):
    """
    GIVEN the JsonGenerator init method
    WHEN we call it with a config containing a valid path to a valid sample
        fields file
    THEN the resulting instance's config should match the input
    AND the field_data attribute should be set
    AND the get_*_fields_json methods should return lists with the correct
        number of records based on the sample fields file contents
    """
    good_config_dict["field_data_path"] = good_sample_fields_file_path
    generator = JsonGenerator(good_config_dict)
    assert generator.config == good_config_dict
    assert generator.field_data is not None
    assert generator.field_data != {}
    assert len(generator.get_bugzilla_fields_json()) == EXPECTED_BZ_FIELD_COUNT
    assert len(generator.get_jira_fields_json()) == EXPECTED_JIRA_FIELD_COUNT


def test_init_bad_file_path(good_config_dict):
    """
    GIVEN the JsonGenerator init method
    WHEN we call it with a config whose field_data_path attribute points to a
        non-existent file
    THEN an IOError should be raised
    """
    good_config_dict["field_data_path"] = "/foobar/file/does/not/exist"
    with pytest.raises(IOError):
        JsonGenerator(good_config_dict)


def test_init_invalid_json(good_config_dict):
    """
    GIVEN the JsonGenerator init method
    WHEN we patch builtins.open to return invalid sample field data
    AND we initialize the class with a good config file
    THEN a JsonGeneratorException should be raised with an appropriate message
    """
    with patch("builtins.open", mock_open(read_data="{}")):
        with pytest.raises(JsonGeneratorException,
                           match="Invalid field data detected"):
            JsonGenerator(good_config_dict)


def test_init_empty_config():
    """
    GIVEN the JsonGenerator init method
    WHEN we call it with an empty config dict
    THEN the config and field_data instance fields should be empty dicts
    AND the get_*_fields_json methods should return empty lists
    """
    generator = JsonGenerator(config={})
    assert generator.config == {}
    assert generator.field_data == {}
    assert generator.get_bugzilla_fields_json() == []
    assert generator.get_jira_fields_json() == []


def test_init_none_config():
    """
    GIVEN the JsonGenerator init method
    WHEN we call it with an empty config dict
    THEN the config attribute should be None
    AND the field_data attribute should be an empty dict
    AND the get_*_fields_json methods should return empty lists
    """
    generator = JsonGenerator(config=None)
    assert generator.config is None
    assert generator.field_data == {}
    assert generator.get_bugzilla_fields_json() == []
    assert generator.get_jira_fields_json() == []


def test_register(good_config_dict, good_sample_fields_file_path):
    """
    GIVEN the static register method
    WHEN we call it with a good config including a path to a valid fields file
    THEN the field_factory module's _json_generator attribute should be set to
        an instance of JsonGenerator
    """
    good_config_dict["field_data_path"] = good_sample_fields_file_path
    JsonGenerator.register(good_config_dict)
    assert isinstance(json_generator.field_factory._json_generator,
                      JsonGenerator)
