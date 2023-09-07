import pytest

from unittest.mock import patch, Mock

from bugjira.field import BugzillaField, JiraField
from bugjira.field_factory import get_bugzilla_fields, get_jira_fields


@pytest.fixture
def mock_bz_field_json():
    return [{"name": "bugzilla"}, {"name": "status"}, {"name": "assignee"}]


@pytest.fixture
def mock_jira_field_json():
    return [{"name": "jira", "jira_field_id": "jira_field_id"},
            {"name": "jira2", "jira_field_id": "jira2_field_id"}]


@pytest.fixture
def mock_json_generator(mock_bz_field_json, mock_jira_field_json):
    mock_generator = Mock()
    attrs = {'get_bugzilla_fields_json.return_value': mock_bz_field_json,
             'get_jira_fields_json.return_value': mock_jira_field_json}
    mock_generator.configure_mock(**attrs)
    return mock_generator


def test_get_bugzilla_fields(mock_json_generator, mock_bz_field_json):
    """
    GIVEN the get_bugzilla_fields method and a json generator that produces
        a known set of valid field input records
    WHEN we call get_bugzilla_fields
    THEN the returned list of BugzillaField objects has the same length as the
        input data
    AND all the returned BugzillaField objects correspond to a record in the
        input data
    """
    with patch("bugjira.field_factory._json_generator", mock_json_generator):
        assert len(get_bugzilla_fields()) == len(mock_bz_field_json)
        for field in get_bugzilla_fields():
            assert isinstance(field, BugzillaField)
            assert field.model_dump() in mock_bz_field_json


def test_get_jira_fields(mock_json_generator, mock_jira_field_json):
    """
    GIVEN the get_jira_fields method and a json generator that produces
        a known set of valid field input records
    WHEN we call get_jira_fields
    THEN the returned list of JiraField objects has the same length as the
        input data
    AND all the returned JiraField objects correspond to a record in the
        input data
    """
    with patch("bugjira.field_factory._json_generator", mock_json_generator):
        assert len(get_jira_fields()) == len(mock_jira_field_json)
        for field in get_jira_fields():
            assert isinstance(field, JiraField)
            assert field.model_dump() in mock_jira_field_json


def test_get_fields_with_none_generator():
    """
    GIVEN the get_bugzilla_fields and get_jira_fields methods
    AND the fields_factory._json_generator attribute set to 'None'
    WHEN we call the methods
    THEN an empty list is returned
    """
    for method in get_bugzilla_fields, get_jira_fields:
        assert method() == []
