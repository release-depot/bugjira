import pytest

from bugjira.util import is_bugzilla_key, is_jira_key


def test_is_key_with_non_str():
    """
    GIVEN the is_bugzilla_key and is_jira_key methods
    WHEN they are called with a non-str input
    THEN a ValueError is raised
    """
    for test in is_bugzilla_key, is_jira_key:
        with pytest.raises(ValueError):
            test(1)


def test_is_bugzilla_key_true(good_bz_keys):
    """
    GIVEN the is_bugzilla_key method
    WHEN it is called with a str that matches the bz id format
    THEN the method returns True
    """
    for key in good_bz_keys:
        assert is_bugzilla_key(key) is True


def test_is_bugzilla_key_false(bad_bz_keys):
    """
    GIVEN the is_bugzilla_key method
    WHEN it is called with a str that doesn't match the bz id format
    THEN the method returns False
    """
    for key in bad_bz_keys:
        assert is_bugzilla_key(key) is False


def test_is_jira_key_true(good_jira_keys):
    """
    GIVEN the is_jira_key method
    WHEN it is called with a str that matches the jira key format
    THEN the method returns True
    """
    for key in good_jira_keys:
        assert is_jira_key(key) is True


def test_is_jira_key_false(bad_jira_keys):
    """
    GIVEN the is_jira_key method
    WHEN it is called with a str that doesn't match the jira key format
    THEN the method returns False
    """
    for key in bad_jira_keys:
        assert is_jira_key(key) is False
