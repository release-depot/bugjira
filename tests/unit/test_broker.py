from unittest.mock import Mock, create_autospec

import pytest
from bugzilla import Bugzilla
from jira import JIRA
from pydantic import ValidationError

import bugjira.broker as broker
from bugjira.broker import (
    Broker,
    BrokerInitException,
    BugzillaBroker,
    JiraBroker,
)


@pytest.fixture(scope="function", autouse=True)
def setup(monkeypatch):
    monkeypatch.setattr(broker, "Bugzilla", create_autospec(Bugzilla))
    monkeypatch.setattr(broker, "JIRA", create_autospec(JIRA))


def test_broker_init_no_backend():
    """
    GIVEN the Broker class' constructor
    WHEN we call it without supplying a backend parameter
    THEN the resulting instance's backend attribute should be None
    """
    broker = Broker(config={})
    assert broker.backend is None


def test_broker_init_with_backend():
    """
    GIVEN the Broker class' constructor
    WHEN we call it with a backend parameter supplied
    THEN the resulting instance's backend attribute should be the one we input
        to the constructor
    """
    backend = Mock()
    broker = Broker(backend=backend)
    assert broker.backend == backend


def test_broker_init_with_no_parameters():
    """
    GIVEN the Broker class' constructor
    WHEN we call it with no parameters
    THEN a BrokerInitException should be raised
    """
    with pytest.raises(BrokerInitException):
        Broker()


def test_broker_init_with_no_config_and_no_backend():
    """
    GIVEN the Broker class' constructor
    WHEN we call it with None for both parameters
    THEN a BrokerInitException should be raised
    """
    with pytest.raises(BrokerInitException):
        Broker(config=None, backend=None)


def test_bugzilla_broker_init_with_valid_config(good_config_dict):
    """
    GIVEN the BugzillaBroker class
    WHEN we instantiate it
    THEN the instance's backend should have a method called 'getbug'
    """
    bzb = BugzillaBroker(config=good_config_dict)
    # We won't check the type here because backend is a Mock created via
    # create_autospec, but we'll just make sure the method name is an attribute
    assert bzb.backend.getbug


def test_bugzilla_broker_init_with_invalid_config():
    """
    GIVEN the Bugjira class' constructor
    WHEN it is called with only an invalid (in this case, empty) config dict
    THEN a ValidationError will be raised
    """
    with pytest.raises(ValidationError):
        BugzillaBroker(config={})


def test_jira_broker_init_with_invalid_config():
    """
    GIVEN the Jira class' constructor
    WHEN it is called with only an invalid (in this case, empty) config dict
    THEN a ValidationError will be raised
    """
    with pytest.raises(ValidationError):
        JiraBroker(config={})


def test_jira_broker_init_with_valid_config(good_config_dict):
    """
    GIVEN the JiraBroker class
    WHEN we instantiate it
    THEN the instance's backend should have a method called 'issue'
    """
    jb = JiraBroker(config=good_config_dict)
    # We won't check the type here because backend is a Mock created via
    # create_autospec, but we'll just make sure the method name is an attribute
    assert jb.backend.issue
