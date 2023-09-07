import os
import pytest
from bugjira.config import Config


@pytest.fixture
def config_defaults():
    _dir = os.path.dirname(os.path.realpath(__file__))
    return _dir


@pytest.fixture()
def good_config_file_path(config_defaults):
    return config_defaults + "/data/config/good_config.json"


@pytest.fixture
def good_config_dict(good_config_file_path):
    return Config.from_config(config_path=good_config_file_path)


@pytest.fixture()
def good_sample_fields_file_path(config_defaults):
    return config_defaults + "/data/sample_fields/sample_fields.json"


@pytest.fixture
def good_bz_keys():
    return ["123456", "1"]


@pytest.fixture
def bad_bz_keys():
    return ["RHOSOR-123", "1a"]


@pytest.fixture
def good_jira_keys():
    return ["RHOSOR-123", "PCTOOLING-654", "test-123", "FOO_123"]


@pytest.fixture
def bad_jira_keys():
    return ["23456", "1a", "PCTOOLING123", "123-abc"]
