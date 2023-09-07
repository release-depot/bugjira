import json
from typing import List

from pydantic import BaseModel, ConfigDict, ValidationError

from bugjira import field_factory
from bugjira.exceptions import JsonGeneratorException
from bugjira.field import BugzillaField, JiraField


def get_generator():
    """Plugin modules must define the get_generator() method, which should
    return a generator class.
    """
    return JsonGenerator


class JsonGenerator:
    """This is the default plugin class that provides json to field_factory
    module for generating lists of BugjiraField objects. It loads its data
    from a json file, specified in the input config dict under the
    "field_data_path" top level key.

    The static `register` method registers the class with the field_factory
    module.

    Replacement plugin classes should implement the `get_bugzilla_fields_json`
    and `get_jira_fields_json` instance methods, as well as the static
    `register` method.
    """
    def __init__(self, config={}):
        self.config = config
        self.field_data = {}
        if config:
            field_data_path = config.get("field_data_path", "")
            if field_data_path:
                with open(field_data_path, "r") as file:
                    field_data = json.load(file)
                    try:
                        # use pydantic class to validate the input data
                        ValidFieldData(**field_data)
                    except ValidationError:
                        raise JsonGeneratorException(
                            "Invalid field data detected"
                        )
                    self.field_data = field_data

    def get_bugzilla_fields_json(self):
        return self.field_data.get("bugzilla_field_data", [])

    def get_jira_fields_json(self):
        return self.field_data.get("jira_field_data", [])

    @staticmethod
    def register(config):
        field_factory.register_json_generator(JsonGenerator, config)


class ValidFieldData(BaseModel):
    """This class defines the valid format for the json data loaded by the
    JsonGenerator class
    """
    model_config = ConfigDict(extra="forbid")
    bugzilla_field_data: List[BugzillaField]
    jira_field_data: List[JiraField]
