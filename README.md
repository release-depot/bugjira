# Bugjira
Bugjira is an abstraction layer library for interacting with either bugzilla or JIRA via their respective python libraries.

## Examples

Bugjira users can perform common operations (lookup, query, modify, etc) on both bugs (bugzilla) and issues (jira) using the Bugjira object.

Configuration is provided with either a dict (see below) or a pathname to a config file containing a json dict (a sample config file is included in `contrib/bugjira.json`):

```python
from bugjira.bugjira import Bugjira
config = {
    "bugzilla": {
        "URL": "https://bugzilla.yourdomain.com",
        "api_key": "your_bugzilla_api_key"},
    "jira": {
        "URL": "https://jira.yourdomain.com",
        "token_auth": "your_jira_personal_access_token"}
 }

bugjira_api = Bugjira(config_dict=config)
```

(Note that the `config_dict` parameter takes precedence; i.e. if you instantiate the Bugjira class with both a config_path and a config_dict parameter, the resulting instance will use the config_dict's values.)

After initializing a Bugjira instance, you can use its methods to look up either bugs or issues. The object returned by the Bugjira instance is of type `bugjira.Issue` which (TODO) allows access to the underlying attributes of the wrapped bug or jira issue:
```python
bz = bugjira_api.get_issue("123456")
assert bz.key == "123456"
```
Instances of `bugjira.Issue` have attributes called `bugzilla` and `jira_issue` that are set by their respective backend broker so that you can easily tell what type of Issue you're dealing with. As a convenience, those attributes are pointers to the wrapped bug or jira issue. So if the Issue class' methods don't give you what you need, you have the actual bug or jira issue whenever you need it:
```python
if bz.bugzilla:
    print(f"Product is: {bz.bugzilla.product})
# You can also use type checking since the backends return subclasses of Issue
if isinstance(bz, bugjira.BugzillaIssue):
    print(f"Product is: {bz.bugzilla.product}")
assert not isinstance(bz, bugjira.JiraIssue)
```

Similarly, if the `bugjira.Bugjira` instance's API doesn't give you what you need, you can easily get a handle to the underlying Bugzilla or JIRA backend API object via the `bugzilla` and `jira_api` attributes and then use it as you like:
```python
bugzilla_api = bugjira_api.bugzilla
actual_bz = bugzilla_api.getbug("123456") # using the Bugzilla api object's getbug
print("Fetched bug #%s:" % actual_bz.id)
```
or
```python
jira_api = bugjira_api.jira
issue = jira_api.get_issue("FOO-123") # using the JIRA api object's get_issue
```

## Field Configuration
Users of the Bugjira library will be able to read and write field contents from `bugjira.Issue` objects uniformly whether the Issue represents a bugzilla bug (`bugjira.BugzillaIssue`) or a JIRA issue (`bugjira.JiraIssue`).

Bugzilla's issue (bug) attributes are relatively static, and they are named and accessed in a straightforward way. JIRA's issue attributes, in contrast, consist of a pre-defined set of attributes (e.g. "issuetype", "status", "assignee") and an arbitrarily large set of custom fields (with identifiers like "customfield_12345678"). Furthermore, the JIRA api requires multiple requests to obtain the necessary metadata to use custom fields.

Since both Bugzilla and JIRA allow field customization, and since it is cumbersome to obtain JIRA custom field metadata dynamically, the Bugjira library will rely on user-supplied configuration information to determine what fields are supported by the user's JIRA and Bugzilla instances. The data Bugjira requires to define fields is specified by the `BugzillaField` and `JiraField` classes in the `bugjira.field` module. Internally, Bugjira uses the `bugjira.field_factory` module as its source of field information.

The `field_factory` module generates `BugzillaField` and `JiraField` objects using json retrieved from a plugin module loaded at runtime. The default plugin is defined by the included `bugjira.json_generator` module, which is specified in the config dict under the "json_generator_module" key. This module defines a class called `JsonGenerator` whose `get_bugzilla_field_json` and `get_jira_field_json` instance methods return json field information. The `bugjira.field_factory` module consumes that json to create lists of `BugzillaField` and `JiraField` objects.

The `bugjira.json_generator.JsonGenerator` class loads its json data from a file whose path is (optionally) specified in the config dict under the "field_data_file_path" key. A sample file is provided in `contrib/sample_fields.json`. The field information in this file is not intended to be comprehensive; if you use the default `bugjira.json_generator` plugin, we encourage you to edit the sample fields file to support your JIRA instance and intended use cases.
