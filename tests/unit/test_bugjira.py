from copy import deepcopy
from unittest.mock import Mock, create_autospec
from xmlrpc.client import Fault

import pytest
from bugzilla import Bugzilla
from jira import JIRA
from jira.exceptions import JIRAError

import bugjira.broker as broker
from bugjira.exceptions import (
    BrokerLookupException, BrokerAddCommentException
)
from bugjira.bugjira import Bugjira
from bugjira.issue import Issue, BugzillaIssue, JiraIssue


@pytest.fixture(scope="function", autouse=True)
def setup(monkeypatch):
    """Patch out the bugzilla.Bugzilla and jira.JIRA constructors
    in the broker module so that we don't attempt to connect to an actual
    backend
    """
    monkeypatch.setattr(broker, "Bugzilla", create_autospec(Bugzilla))
    monkeypatch.setattr(broker, "JIRA", create_autospec(JIRA))


@pytest.fixture(scope="function")
def sandboxed_bugjira(good_config_dict):
    return Bugjira(config_dict=good_config_dict)


def test_init_with_config_dict(good_config_dict):
    """
    GIVEN the Bugjira class' constructor
    WHEN we call it with a valid config dict
    THEN the resulting Bugjira instance's config attribute will be the dict
        we input to the constructor
    AND the broker and backend attributes should be present
    """
    bugjira = Bugjira(config_dict=good_config_dict)
    assert bugjira.config == good_config_dict
    assert bugjira._bugzilla_broker
    assert bugjira._jira_broker
    assert bugjira.bugzilla
    assert bugjira.jira


def test_init_with_config_path(good_config_file_path, good_config_dict):
    """
    GIVEN the Bugjira class' constructor
    WHEN we call it with a path to a known good config file
    THEN the resulting instance's config attribute should be equivalent to the
        contents of the config file
    AND the broker and backend attributes should be present
    """
    bugjira = Bugjira(config_path=good_config_file_path)
    assert bugjira.config == good_config_dict
    assert bugjira._bugzilla_broker
    assert bugjira._jira_broker
    assert bugjira.bugzilla
    assert bugjira.jira


def test_init_with_both_path_and_dict(good_config_file_path, good_config_dict):
    """
    GIVEN the Bugjira class' constructor
    WHEN we call it with a path and a dict
    THEN the resulting instance's config attribute should be equivalent to the
        contents of the config dict
    """
    # Assumption: the good_config_file_path and good_config_dict should produce
    # the same dict contents. So if we deepcopy the good_config_dict, edit
    # the result, and pass the modified dict into the Bugjira constructor,
    # we can test for equivalence and difference as below.
    edited_dict = deepcopy(good_config_dict)
    edited_dict["bugzilla"]["URL"] = "foo"
    bugjira = Bugjira(
        config_path=good_config_file_path, config_dict=edited_dict
    )
    assert bugjira.config != good_config_dict
    assert bugjira.config == edited_dict


def test_init_with_no_parameters():
    """
    GIVEN the Bugjira class' constructor
    WHEN we call it with no parameters
    THEN a BrokerInitException should be raised
    """
    with pytest.raises(broker.BrokerInitException):
        Bugjira()


def test_init_with_only_bz_backend_supplied():
    """
    GIVEN the Bugjira class' constructor
    WHEN we call it with only the bugzilla parameter supplied
    THEN a BrokerInitException should be raised
    """
    with pytest.raises(broker.BrokerInitException):
        Bugjira(bugzilla=Mock())


def test_init_with_only_jira_backend_supplied():
    """
    GIVEN the Bugjira class' constructor
    WHEN we call it with only the jira parameter supplied
    THEN a BrokerInitException should be raised
    """
    with pytest.raises(broker.BrokerInitException):
        Bugjira(jira=Mock())


def test_init_with_both_backends_and_config(good_config_dict):
    """
    GIVEN the Bugjira class' constructor
    WHEN we call it with bugzilla and jira parameters and a valid config
    THEN no exception is raised
    AND the instance backends are the same as what we passed to the constructor
    """
    bugzilla = Mock()
    jira = Mock()
    bugjira = Bugjira(
        config_dict=good_config_dict, bugzilla=bugzilla, jira=jira
    )
    assert bugjira.bugzilla == bugzilla
    assert bugjira.jira == jira


def test_init_with_both_backends_and_no_config():
    """
    GIVEN the Bugjira class' constructor
    WHEN we call it with bugzilla and jira parameters and a no config
    THEN no exception is raised
    AND the instance backends are the same as what we passed to the constructor
    """
    bugzilla = Mock()
    jira = Mock()
    bugjira = Bugjira(bugzilla=bugzilla, jira=jira)
    assert bugjira.bugzilla == bugzilla
    assert bugjira.jira == jira


def test_get_broker_with_bugzilla_id(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance's _get_broker method
    WHEN we call it with a key string that represents a bugzilla bug id
    THEN the instance's _bugzilla_broker attribute should be returned
    """
    broker = sandboxed_bugjira._get_broker("123456")
    assert broker == sandboxed_bugjira._bugzilla_broker


def test_get_broker_with_jira_issue_id(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance's _get_broker method
    WHEN we call it with a key string that represents a jira issue key
    THEN the instance's _jira_broker attribute should be returned
    """
    broker = sandboxed_bugjira._get_broker("FOO-123")
    assert broker == sandboxed_bugjira._jira_broker


def test_get_broker_with_invalid_string_key(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance's _get_broker method
    WHEN we call it with a key string that is neither a bugzilla or jira key
    THEN a ValueError should be raised
    """
    with pytest.raises(ValueError):
        sandboxed_bugjira._get_broker("BADKEY123")


def test_get_issue_with_non_string_key(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance's get_issue method
    WHEN we call it with a non-string parameter
    THEN a ValueError is raised
    """
    with pytest.raises(ValueError):
        sandboxed_bugjira.get_issue(1)


def test_add_comment_non_issue(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance
    WHEN we call add_comment with a None value for the 'issue' parameter
    THEN a ValueError should be raised
    """
    with pytest.raises(ValueError,
                       match="issue must be an Issue"):
        sandboxed_bugjira.add_comment(None, "")


def test_add_comment_non_string_comment(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance
    WHEN we call add_comment with a None value for the 'comment' parameter
    THEN a ValueError should be raised
    """
    with pytest.raises(ValueError,
                       match="comment must be a str"):
        sandboxed_bugjira.add_comment(Issue(key="foo"),
                                      None)


def test_add_comment_good_bugzilla(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance
    WHEN we call add_comment with a BugzillaIssue and comment string
    THEN the bugzilla backend's build_update and update_bugs methods should
        each be invoked once
    """
    comment_text = "This is a sample comment"
    key = "123456"
    issue = BugzillaIssue(key=key)
    sandboxed_bugjira.add_comment(issue, comment_text)
    assert sandboxed_bugjira.bugzilla.build_update.call_count == 1
    assert sandboxed_bugjira.bugzilla.update_bugs.call_count == 1


def test_add_comment_bugzilla_exception(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance whose bugzilla backend's update_bugs method
        raises an Exception
    WHEN we call add_comment
    THEN a BrokerAddCommentException should be raised
    """
    msg = "Exception raised"
    sandboxed_bugjira.bugzilla.update_bugs.side_effect = Exception(msg)
    comment_text = "This is a sample comment"
    key = "123456"
    issue = BugzillaIssue(key=key)
    with pytest.raises(BrokerAddCommentException,
                       match=msg):
        sandboxed_bugjira.add_comment(issue, comment_text)


def test_add_comment_good_jira(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance
    WHEN we call add_comment with a JiraIssue and comment string
    THEN the jira backend's add_comment method should be invoked once
    """
    comment_text = "This is a sample comment"
    key = "FOO-123"
    issue = JiraIssue(key=key)
    sandboxed_bugjira.add_comment(issue, comment_text)
    assert sandboxed_bugjira.jira.add_comment.call_count == 1


def test_add_comment_jira_exception(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance whose jira backend's add_comment method
        raises an Exception
    WHEN we call add_comment
    THEN a BrokerAddCommentException should be raised
    """
    msg = "Exception raised"
    sandboxed_bugjira.jira.add_comment.side_effect = Exception(msg)
    comment_text = "This is a sample comment"
    key = "FOO-123"
    issue = JiraIssue(key=key)
    with pytest.raises(BrokerAddCommentException,
                       match=msg):
        sandboxed_bugjira.add_comment(issue, comment_text)


def test_get_issue_good_bugzilla(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance
    WHEN we invoke the get_issue method with a BZ number
    THEN it should return an instance of Issue with a non-None bugzilla
        attribute and a key matching the input
    AND the instance's bugzilla attribute should have had its getbug method
        invoked once
    """
    key = "123456"
    issue = sandboxed_bugjira.get_issue(key)
    assert isinstance(issue, BugzillaIssue)
    assert issue.bugzilla
    assert not issue.jira_issue
    assert issue.key == key
    assert sandboxed_bugjira.bugzilla.getbug.call_count == 1


def test_get_issue_bad_bugzilla(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance
    WHEN we invoke the get_issue method with a BZ number using a bug id that is
        known not to correspond to any bug on the remote bugzilla service
    THEN a BrokerLookupException exception should be raised
    """
    sandboxed_bugjira.bugzilla.getbug.side_effect = Fault(
        "Fault 101", "Bug #XXX does not exist."
    )
    with pytest.raises(BrokerLookupException):
        sandboxed_bugjira.get_issue("123")


def test_get_issue_good_jira_issue(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance
    WHEN we invoke the get_issue method with a Jira issue key
    THEN it should return an instance of Issue with a non-None jira_issue
        attribute and a key matching the input
    AND the instance's jira attribute should have had its issue method invoked
        once
    """
    key = "FOO-123"
    issue = sandboxed_bugjira.get_issue(key)
    assert isinstance(issue, JiraIssue)
    assert issue.jira_issue
    assert not issue.bugzilla
    assert issue.key == key
    assert sandboxed_bugjira.jira.issue.call_count == 1


def test_get_issue_bad_jira_issue(sandboxed_bugjira):
    """
    GIVEN a Bugjira instance
    WHEN we invoke the get_issue method with a JIRA issue key using a key that
        is known not to correspond to any issue on the remote bugzilla service
    THEN a BrokerLookupException exception should be raised
    """
    sandboxed_bugjira.jira.issue.side_effect = JIRAError
    with pytest.raises(BrokerLookupException):
        sandboxed_bugjira.get_issue("FOO-666")
