import pytest
from unittest.mock import mock_open, patch

from bugjira.common import BUGZILLA, JIRA
from bugjira.exceptions import FieldDataGeneratorException
from bugjira.field_data_generator import (
    FieldDataGenerator, BugzillaFieldDataGenerator, JiraFieldDataGenerator,
    FieldDataGeneratorFactory
)

EXPECTED_BZ_FIELD_COUNT = 3
EXPECTED_JIRA_FIELD_COUNT = 2

GENERATOR_CLASSES = [BugzillaFieldDataGenerator, JiraFieldDataGenerator]
KEYS = [BUGZILLA, JIRA]


def test_init_good_config(good_config_dict, good_sample_fields_file_path):
    """
    GIVEN the FieldDataGenerator init method
    WHEN we call it with a config containing a valid path to a valid sample
        fields file
    THEN the field_data attribute should be set
    """
    good_config_dict["field_data_path"] = good_sample_fields_file_path
    generator = FieldDataGenerator(good_config_dict)
    assert generator.field_data is not None
    assert generator.field_data != {}


def test_init_bad_data(good_config_dict):
    """
    GIVEN the FieldDataGenerator class
    WHEN the data it loads fails the ValidFieldData validation
    THEN a FieldDataGeneratorException is raised
    """
    with patch("bugjira.field_data_generator.open",
               mock_open(read_data="{}")):
        with pytest.raises(FieldDataGeneratorException):
            FieldDataGenerator(good_config_dict)


def test_bugzilla_get_field_data(good_config_dict,
                                 good_sample_fields_file_path):
    """
    GIVEN the BugzillaFieldDataGenerator class
    WHEN we instantiate it with a good config with a path to a good data file
    THEN the get_field_data method should return the expected number of fields
    """
    good_config_dict["field_data_path"] = good_sample_fields_file_path
    generator = BugzillaFieldDataGenerator(good_config_dict)
    assert len(generator.get_field_data()) == EXPECTED_BZ_FIELD_COUNT


def test_jira_get_field_data(good_config_dict, good_sample_fields_file_path):
    """
    GIVEN the JiraFieldDataGenerator class
    WHEN we instantiate it with a good config with a path to a good data file
    THEN the get_field_data method should return the expected number of fields
    """
    good_config_dict["field_data_path"] = good_sample_fields_file_path
    generator = JiraFieldDataGenerator(good_config_dict)
    assert len(generator.get_field_data()) == EXPECTED_JIRA_FIELD_COUNT


def test_get_field_data_generator():
    """
    GIVEN a new instance of FieldDataGeneratorFactory
    WHEN we call the get_field_data_generator method twice
    THEN the _get_field_data_plugin_instance method should be called only once
    AND the object that is returned should match what is returned by
        the _get_field_data_plugin_instance method
    """
    return_value = "return_value"
    factory = FieldDataGeneratorFactory()
    with patch.object(FieldDataGeneratorFactory,
                      "_get_field_data_plugin_instance",
                      return_value=return_value) as patched:
        foo = factory.get_field_data_generator("foobar", {})
        assert foo == return_value
        foo = factory.get_field_data_generator("foobar", {})
        assert foo == return_value
        assert patched.call_count == 1


@pytest.mark.parametrize("key", KEYS)
def test_get_plugin_name_from_config(good_config_dict, key):
    """
    GIVEN an instance of FieldDataGeneratorFactory
    WHEN we call _get_plugin_name_from_config with good keys and a good config
    THEN a non-empty string should be returned
    """
    factory = FieldDataGeneratorFactory()
    result = factory._get_plugin_name_from_config(key, good_config_dict)
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_plugin_name_from_config_bad_key():
    """
    GIVEN an instance of FieldDataGeneratorFactory
    WHEN we call the _get_plugin_name_from_config method with an invalid key
    THEN a ValueError is raised
    """
    factory = FieldDataGeneratorFactory()
    with pytest.raises(ValueError):
        factory._get_plugin_name_from_config("foobar_key", {})
