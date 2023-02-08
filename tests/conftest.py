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
