import pytest
from unittest.mock import patch
from typing import List

from bugjira.common import BUGZILLA, JIRA
from bugjira.field_data_generator import (
    BugzillaFieldDataGenerator,
    JiraFieldDataGenerator,
    FieldDataGeneratorFactory
)
from bugjira.field_generator import FieldGenerator, FieldGeneratorFactory
from bugjira.field import BugzillaField, JiraField


def get_field_instance_data_dict_from_field_class(field_class):
    """A convenience method that uses introspection to generate a dict of
    valid parameters for the attributes in the passed-in BugjiraField subclass.
    This dict can then be used to create an instance of the class without
    raising a pydantic validation error. Note that only simple attribute types
    are supported currently. If/when the *Field classes have attributes of
    other types, then the 'values' dict will need to be updated here.
    """
    if field_class not in [BugzillaField, JiraField]:
        raise ValueError()

    values = {
        int: 1,
        float: 2.1,
        str: "a string"
    }
    return {a[0]: values.get(a[1].annotation) for a
            in iter(field_class.model_fields.items())}


class StubbedFieldGeneratorFactory(FieldDataGeneratorFactory):
    """This class is used to patch out the FieldDataGeneratorFactory. It
    instantiates the default FieldDataGenerator plugins and pre-populates the
    dict from which the get_field_data_generator method retrieves them. It
    uses the get_field_instance_dict_from_pydantic_class method to pre-load
    some valid field data that the FieldDataGenerator subclasses can return
    via the get_field_data method.
    """
    def __init__(self):
        field_data = {
            "bugzilla_field_data": [
                get_field_instance_data_dict_from_field_class(BugzillaField)
            ],
            "jira_field_data": [
                get_field_instance_data_dict_from_field_class(JiraField)
            ]
        }

        bzfg = BugzillaFieldDataGenerator({})
        jfg = JiraFieldDataGenerator({})
        for instance in bzfg, jfg:
            instance.field_data = field_data

        self.field_data_generators = {
            BUGZILLA: bzfg,
            JIRA: jfg
        }


@pytest.fixture(autouse=True)
def patch_data_generator_factory():
    """This fixture replaces the field_data_factory used in the field_generator
    module. In its place we put an instance of StubbedFieldGeneratorFactory.
    """
    patcher = patch("bugjira.field_generator.field_data_generator_factory",
                    StubbedFieldGeneratorFactory())
    patcher.start()
    yield
    patcher.stop()


@pytest.mark.parametrize("generator_type,field_class,data_generator_class",
                         [
                             (BUGZILLA, BugzillaField,
                              BugzillaFieldDataGenerator),
                             (JIRA, JiraField,
                              JiraFieldDataGenerator)
                         ])
def test_field_generator_init(generator_type, field_class,
                              data_generator_class):
    """
    GIVEN the FieldGenerator class
    WHEN we initialize it
    THEN the instance's config, field_data_generator, and field_class
        attributes should be set to expected values
    """
    config = {"expected": "config"}
    fg = FieldGenerator(generator_type, config)
    assert fg.config == config
    assert isinstance(fg.field_data_generator, data_generator_class)
    assert fg.field_class == field_class


def test_field_generator_init_bad_generator_type():
    """
    GIVEN the FieldGenerator class
    WHEN we call init with an invalid generator_type
    THEN a ValueError is raised
    """
    with pytest.raises(ValueError):
        FieldGenerator(generator_type="bad generator type",
                       config={})


@pytest.mark.parametrize("generator_type,expected_value",
                         [(BUGZILLA, BugzillaField),
                          (JIRA, JiraField)])
def test_get_field_class(generator_type, expected_value):
    """
    GIVEN an instance of the FieldGenerator class
    WHEN we call _get_field_class with a valid generator_type
    THEN the correct BugjiraField subclass associated with the type is returned
    """
    fg = FieldGenerator(generator_type, {})
    assert fg._get_field_class(generator_type) == expected_value


def test_get_field_class_bad_key():
    """
    GIVEN an instance of the FieldGenerator class
    WHEN we call _get_field_class with an invalid generator_type
    THEN a ValueError is raised
    """
    # first instantiate the FieldGenerator with a good generator_type
    fg = FieldGenerator(BUGZILLA, {})
    # now call _get_field_class with a bad generator_type parameter
    with pytest.raises(ValueError):
        fg._get_field_class("bad key")


@pytest.mark.parametrize("generator_type,field_type",
                         [(BUGZILLA, BugzillaField), (JIRA, JiraField)])
def test_get_fields(generator_type, field_type):
    """
    GIVEN an instance of the FieldGenerator class
    WHEN we call its get_fields method
    THEN the returned value should be a List containing instances of the
        correct BugjiraField subclass corresponding to the generator_type used
        to instantiate the FieldGenerator class
    """
    bz = FieldGenerator(generator_type, {})
    fields = bz.get_fields()
    assert isinstance(fields, List)
    for field in fields:
        assert isinstance(field, field_type)


@pytest.mark.parametrize("generator_type,expected_field_class",
                         [(BUGZILLA, BugzillaField),
                          (JIRA, JiraField)])
def test_get_field_generator(generator_type, expected_field_class):
    """
    GIVEN an instance of the FieldGeneratorFactory class
    WHEN we call get_field_generator with a valid generator_type
    THEN a FieldGenerator instance is returned whose field_class attribute is
        the correct BugjiraField subclass for the generator_type
    """
    fgf = FieldGeneratorFactory()
    generator = fgf.get_field_generator(generator_type, {})
    assert isinstance(generator, FieldGenerator)
    assert generator.field_class == expected_field_class
