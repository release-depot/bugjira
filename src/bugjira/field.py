from pydantic import BaseModel, ConfigDict, constr

"""The objects in this module are used internally to represent field
configuration information for the bugzilla and jira backends used by bugjira.
"""


class BugjiraField(BaseModel):
    """The base field class
    """
    model_config = ConfigDict(extra="forbid")
    name: constr(strip_whitespace=True, min_length=1)


class BugzillaField(BugjiraField):
    pass


class JiraField(BugjiraField):
    jira_field_id: constr(strip_whitespace=True, min_length=1)
