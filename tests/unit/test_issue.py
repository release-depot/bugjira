import pytest
from pydantic import ValidationError

from bugjira.issue import BugzillaIssue, JiraIssue


def test_good_bz_keys(good_bz_keys):
    """
    GIVEN a set of well-formatted bz keys
    WHEN we create a BugzillaIssue with each key
    THEN no ValidationError is raised and the issue key matches the input key
    """
    for key in good_bz_keys:
        issue = BugzillaIssue(key=key)
        assert issue.key == key


def test_bad_bz_keys(bad_bz_keys):
    """
    GIVEN a set of poorly-formatted bz keys
    WHEN we create a BugzillaIssue with each key
    THEN a ValidationError is raised
    """
    for key in bad_bz_keys:
        with pytest.raises(ValidationError):
            BugzillaIssue(key=key)


def test_good_jira_keys(good_jira_keys):
    """
    GIVEN a set of well-formatted jira keys
    WHEN we create a JiraIssue with each key
    THEN no ValidationError is raised and the issue key matches the input key
    """
    for key in good_jira_keys:
        issue = JiraIssue(key=key)
        assert issue.key == key


def test_bad_jira_keys(bad_jira_keys):
    """
    GIVEN a set of poorly-formatted jira keys
    WHEN we create a JiraIssue with each key
    THEN a ValidationError is raised
    """
    for key in bad_jira_keys:
        with pytest.raises(ValidationError):
            JiraIssue(key=key)
