import abc
import json
from typing import List

from pydantic import BaseModel, ConfigDict, ValidationError
from stevedore import driver

from bugjira.common import BUGZILLA, JIRA, PLUGIN_NAMESPACE
from bugjira.exceptions import FieldDataGeneratorException
from bugjira.field import BugzillaField, JiraField


class ValidFieldData(BaseModel):
    """This class defines the valid format for the json data loaded by the
    FieldDataGenerator classes in this module
    """
    model_config = ConfigDict(extra="forbid")
    bugzilla_field_data: List[BugzillaField]
    jira_field_data: List[JiraField]


class FieldDataGeneratorInterface(metaclass=abc.ABCMeta):
    """This abstract base class represents the interface that
    FieldDataGenerator classes should implement. Plugin classes for generating
    field data should implement the get_field_data method.
    """

    @abc.abstractmethod
    def __init__(self, config):
        """Init method"""

    @abc.abstractmethod
    def get_field_data(self) -> List:
        """Return the field data as an Iterable

        :return: List of raw field data to be used to instantiate subclasses of
            the BugjiraField class
        :rtype: List
        """


class FieldDataGenerator(FieldDataGeneratorInterface):
    """This is the superclass for the default/provided FieldDataGenerator
    plugin classes, BugzillaFieldDataGenerator and JiraFieldDataGenerator.
    Both subclasses use the same sample json field data file, so we load that
    data in the superclass's __init__ method.
    """

    def __init__(self, config):
        self.field_data = {}
        if config:
            field_data_path = config.get("field_data_path", "")
            if field_data_path:
                with open(field_data_path, "r") as file:
                    field_data = json.load(file)
                    try:
                        # use pydantic class to validate the input data
                        ValidFieldData(**field_data)
                    except ValidationError as ve:
                        raise FieldDataGeneratorException(
                            "Invalid field data detected"
                        ) from ve
                    self.field_data = field_data

    def get_field_data(self) -> List:
        # override in subclasses
        pass


class BugzillaFieldDataGenerator(FieldDataGenerator):
    """This is the default plugin class for generating field data that can be
    used to instantiate BugzillaField objects
    """

    def get_field_data(self) -> List:
        return self.field_data.get("bugzilla_field_data", [])


class JiraFieldDataGenerator(FieldDataGenerator):
    """This is the default plugin class for generating field data that can be
    used to instantiate JiraField objects
    """

    def get_field_data(self) -> List:
        return self.field_data.get("jira_field_data", [])


class FieldDataGeneratorFactory:
    """Factory class that returns the FieldDataGenerator associated with the
    input generator_type. Uses stevedore's DriverManager to load an instance of
    the correct plugin class. The DriverManager looks in the namespace defined
    in common.PLUGIN_NAMESPACE for the plugin named in the bugjira config file.
    """

    def __init__(self):
        self.field_data_generators = {}

    def get_field_data_generator(self,
                                 generator_type,
                                 config) -> FieldDataGenerator:
        """Returns the FieldDataGenerator associated with the input
        generator_type. Uses the _get_field_data_plugin_instance to get an
        instance if it is not already present in the field_data_generators
        dict.

        :param generator_type: A generator type
        :type generator_type: str
        :param config: A valid bugjira config dict
        :type config: dict
        :return: The FieldDataGenerator associated with the generator type
        :rtype: FieldDataGenerator
        """
        generator = self.field_data_generators.get(generator_type, None)
        if not generator:
            generator = self._get_field_data_plugin_instance(generator_type,
                                                             config)
            self.field_data_generators[generator_type] = generator
        return generator

    def _get_field_data_plugin_instance(self,
                                        generator_type,
                                        config) -> FieldDataGeneratorInterface:
        """Return an instance implementing the FieldDataGeneratorInterface that
        matches the generator_type desired.

        :param generator_type: The desired data generator type
        :type generator_type: str
        :param config: A valid bugjira config dict
        :type config: dict
        :return: A FieldDataGenerator instance corresponding to the generator
            type
        :rtype: FieldDataGeneratorInterface
        """
        plugin_name = self._get_plugin_name_from_config(generator_type,
                                                        config)
        # Use stevedore to load the plugin class and instantiate it using
        # the supplied config dict
        dm = driver.DriverManager(namespace=PLUGIN_NAMESPACE,
                                  name=plugin_name,
                                  invoke_on_load=True,
                                  invoke_args=(config,))
        return dm.driver

    def _get_plugin_name_from_config(self, generator_type, config) -> str:
        """Return the plugin name defined in the supplied config that
        corresponds to the desired generator type.

        :param generator_type: The desired generator type
        :type generator_type: str
        :param config: A valid bugjira config dict
        :type config: dict
        :raises ValueError: Raised in an invalid generator type is supplied
        :return: The name of the plugin defined the config file for the given
            generator type
        :rtype: str
        """
        if generator_type == BUGZILLA:
            return config.get("bugzilla").get("field_data_plugin_name")
        elif generator_type == JIRA:
            return config.get("jira").get("field_data_plugin_name")
        else:
            raise ValueError(generator_type)


factory = FieldDataGeneratorFactory()
