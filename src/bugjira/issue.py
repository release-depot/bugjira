from typing import Any

from pydantic import BaseModel, validator

from bugjira.util import is_bugzilla_key, is_jira_key


class Issue(BaseModel):
    """BaseModel representing either a bugzilla bug or a jira issue.
    Future refactoring will allow access to the bug/issue's attributes
    via instances of this class.
    """

    key: str
    bugzilla: Any
    jira_issue: Any


class BugzillaIssue(Issue):
    @validator("key")
    def validate_key(cls, key):
        assert is_bugzilla_key(key)
        return key


class JiraIssue(Issue):
    @validator("key")
    def validate_key(cls, key):
        assert is_jira_key(key)
        return key
