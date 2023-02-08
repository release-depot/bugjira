from typing import Any

from pydantic import BaseModel


class Issue(BaseModel):
    """BaseModel representing either a bugzilla bug or a jira issue.
    Future refactoring will allow access to the bug/issue's attributes
    via instances of this class.
    """

    key: str
    bugzilla: Any
    jira_issue: Any


class BugzillaIssue(Issue):
    pass


class JiraIssue(Issue):
    pass
