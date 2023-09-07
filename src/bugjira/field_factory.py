from bugjira.field import BugzillaField, JiraField

_json_generator = None


def register_json_generator(generator, config):
    """Registers a generator class to serve as the source for json that
    specifies field configuration data.

    :param generator: The generator to register
    :type generator: class
    :param config: The config to use when instantiating the generator class
    :type config: dict
    """
    global _json_generator
    _json_generator = generator(config=config)


def get_bugzilla_fields() -> list[BugzillaField]:
    fields = []
    if _json_generator is not None:
        for field_data in _json_generator.get_bugzilla_fields_json():
            fields.append(BugzillaField(**field_data))
    return fields


def get_jira_fields() -> list[JiraField]:
    fields = []
    if _json_generator is not None:
        for field_data in _json_generator.get_jira_fields_json():
            fields.append(JiraField(**field_data))
    return fields
