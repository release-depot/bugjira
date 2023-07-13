from copy import deepcopy

import pytest
from pydantic.error_wrappers import ValidationError

from bugjira.config import Config


def test_config_good_json(config_defaults):
    """
    GIVEN a json file containing a valid definition of a Bugjira config dict
    WHEN we call Config.from_config with its pathname
    THEN no exception is raised
    """
    config = Config.from_config(
        config_path=(config_defaults + "/data/config/good_config.json")
    )
    assert config is not None


def test_config_good_dict(good_config_dict):
    """
    GIVEN a well-defined dict containing a Bugjira config
    WHEN we call Config.from_config using the dict as the config_dict
    THEN no exception is raised
    AND the dict returned is the dict that was passed in
    """
    assert Config.from_config(config_dict=good_config_dict) == good_config_dict


def test_config_extra_top_level_value(good_config_dict):
    """
    GIVEN a dict containing a Bugjira config with an extra top-level setting
    WHEN we call Config.from_config using the dict as the config_dict
    THEN a ValidationError is raised with the appropriate error message
    """
    bad_config = deepcopy(good_config_dict)
    bad_config["foo"] = "bar"

    with pytest.raises(ValidationError) as excinfo:
        Config.from_config(config_dict=bad_config)

    assert len(excinfo.value.errors()) == 1
    error = excinfo.value.errors()[0]
    assert error.get("loc") == ("config_dict", "foo")
    assert error.get("msg") == "Extra inputs are not permitted"
    assert error.get("type") == "extra_forbidden"


def test_config_extra_bugzilla_value(good_config_dict):
    """
    GIVEN a dict containing a Bugjira config with an extra bugzilla setting
    WHEN we call Config.from_config using the dict as the config_dict
    THEN a ValidationError is raised with the appropriate error message
    """
    bad_config = deepcopy(good_config_dict)
    bad_config["bugzilla"]["foo"] = "bar"

    with pytest.raises(ValidationError) as excinfo:
        Config.from_config(config_dict=bad_config)

    assert len(excinfo.value.errors()) == 1
    error = excinfo.value.errors()[0]
    assert error.get("loc") == ("config_dict", "bugzilla", "foo")
    assert error.get("msg") == "Extra inputs are not permitted"
    assert error.get("type") == "extra_forbidden"


def test_config_extra_jira_value(good_config_dict):
    """
    GIVEN a dict containing a Bugjira config with an extra jira setting
    WHEN we call Config.from_config using the dict as the config_dict
    THEN a ValidationError is raised with the appropriate error message
    """
    bad_config = deepcopy(good_config_dict)
    bad_config["jira"]["foo"] = "bar"

    with pytest.raises(ValidationError) as excinfo:
        Config.from_config(config_dict=bad_config)

    assert len(excinfo.value.errors()) == 1
    error = excinfo.value.errors()[0]
    assert error.get("loc") == ("config_dict", "jira", "foo")
    assert error.get("msg") == "Extra inputs are not permitted"
    assert error.get("type") == "extra_forbidden"


def test_config_missing_value(good_config_dict):
    """
    GIVEN a dict containing a Bugjira config with one missing key
    WHEN we call Config.from_config using the dict as the config_dict
    THEN a ValidationError is raised with the appropriate error message
    """
    bad_config = deepcopy(good_config_dict)
    bad_config["jira"].pop("token_auth")
    with pytest.raises(ValidationError) as excinfo:
        Config.from_config(config_dict=bad_config)

    assert len(excinfo.value.errors()) == 1
    error = excinfo.value.errors()[0]
    assert error.get("loc") == ("config_dict", "jira", "token_auth")
    assert error.get("msg") == "Field required"
    assert error.get("type") == "missing"


def test_config_empty_value(good_config_dict):
    """
    GIVEN a dict containing a Bugjira config with one empty string value
    WHEN we call Config.from_config using the dict as the config_dict
    THEN a ValidationError is raised with the appropriate error message
    """
    bad_config = deepcopy(good_config_dict)
    bad_config["jira"]["token_auth"] = ""
    with pytest.raises(ValidationError) as excinfo:
        Config.from_config(config_dict=bad_config)

    assert len(excinfo.value.errors()) == 1
    error = excinfo.value.errors()[0]
    assert error.get("ctx").get("min_length") == 1
    assert error.get("loc") == ("config_dict", "jira", "token_auth")


def test_config_empty_values(config_defaults):
    """
    GIVEN a json file containing a a Bugjira config with all empty strings for
        values
    WHEN we call Config.from_config with the path to the file
    THEN a ValidationError is raised showing all the values were missing
    """
    with pytest.raises(ValidationError) as excinfo:
        Config.from_config(
            config_path=(config_defaults + "/data/config/missing_config.json")
        )
    for error in excinfo.value.errors():
        assert error.get("type") == "string_too_short"
        assert error.get("ctx").get("min_length") == 1


def test_config_no_file(config_defaults):
    """
    GIVEN a filepath pointing to a non-existent file
    WHEN we call Config.from_config using the filepath as the config_path
    THEN a FileNotFoundError is raised
    """
    with pytest.raises(FileNotFoundError):
        Config.from_config(
            config_path=(config_defaults + "/data/config/does_not_exist.json")
        )


def test_config_both_path_and_dict(good_config_file_path, good_config_dict):
    """
    GIVEN a path to a valid config file, and a dict that varies slightly from
        the file's config data
    WHEN the get_config method is called using these non-None values for both
        the config_path and config_dict parameters
    THEN the config dict returned by get_config should match the config dict
    """
    # First grab the config_dict from the good config path,
    # copy it, and change a value in the copy
    edited_dict = deepcopy(good_config_dict)
    edited_dict["bugzilla"]["URL"] = "foo"
    # Now call get_config with both the path and the edited dict
    result = Config.from_config(
        config_path=good_config_file_path, config_dict=edited_dict
    )
    # show that the returned dict from get_config matches the one we get from
    # the config_dict
    assert result == edited_dict
    assert result != good_config_dict


def test_config_no_params():
    """
    GIVEN the from_config method
    WHEN we call it with no parameters
    THEN a ValueError should be raised
    """
    with pytest.raises(ValueError):
        Config.from_config()
