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


@pytest.mark.parametrize("key", ["123456", "1"])
def test_is_bugzilla_key_true(key):
    """
    GIVEN the is_bugzilla_key method
    WHEN it is called with a str that matches the bz id format
    THEN the method returns True
    """
    assert is_bugzilla_key(key) is True


@pytest.mark.parametrize("key", ["RHOSOR-123", "1a"])
def test_is_bugzilla_key_false(key):
    """
    GIVEN the is_bugzilla_key method
    WHEN it is called with a str that doesn't match the bz id format
    THEN the method returns False
    """
    assert is_bugzilla_key(key) is False


@pytest.mark.parametrize("key", ["RHOSOR-123", "PCTOOLING-654", "test-123"])
def test_is_jira_key_true(key):
    """
    GIVEN the is_jira_key method
    WHEN it is called with a str that matches the jira key format
    THEN the method returns True
    """
    assert is_jira_key(key) is True


@pytest.mark.parametrize("key", ["23456", "1a", "PCTOOLING123", "123-abc"])
def test_is_jira_key_false(key):
    """
    GIVEN the is_jira_key method
    WHEN it is called with a str that doesn't match the jira key format
    THEN the method returns False
    """
    assert is_jira_key(key) is False
