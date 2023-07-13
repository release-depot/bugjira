from typing import Any

from pydantic import BaseModel, field_validator

from bugjira.util import is_bugzilla_key, is_jira_key


class Issue(BaseModel):
    """BaseModel representing either a bugzilla bug or a jira issue.
    Future refactoring will allow access to the bug/issue's attributes
    via instances of this class.
    """

    key: str
    bugzilla: Any = None
    jira_issue: Any = None


class BugzillaIssue(Issue):
    @field_validator("key")
    def validate_key(cls, key):
        if not is_bugzilla_key(key):
            raise ValueError(f"{key} is not a \
                valid bugzilla key")
        return key


class JiraIssue(Issue):
    @field_validator("key")
    def validate_key(cls, key):
        if not is_jira_key(key):
            raise ValueError(f"{key} is not a \
                valid JIRA key")
        return key
