# Bugjira
Bugjira is an abstraction layer library for interacting with either bugzilla or JIRA via their respective python libraries.

## Examples

Bugjira users can perform common operations (lookup, query, modify, etc) on both bugs (bugzilla) and issues (jira) using the Bugjira object.

Configuration is provided with either a dict (see below) or a pathname to a bugjira config file containing a json dict (a sample config file is included in `contrib/bugjira.json`).

At a minimum, you will need to set the "field_data_path" config entry to point to a file containing valid field configuration information. See the [Field Configuration](#field-configuration) section below for more details. Once you have done that, you can create a bugjira instance like so:

```python
from bugjira.bugjira import Bugjira
config = {
    "bugzilla": {
        "URL": "https://bugzilla.redhat.com",
        "api_key": "your_api_key_here",
        "field_data_plugin_name": "default_bugzilla_field_data_plugin"
    },
    "jira": {
        "URL": "https://issues.redhat.com",
        "token_auth": "your_personal_auth_token_here",
        "field_data_plugin_name": "default_jira_field_data_plugin"
    },
    "field_data_path": "/path/to/contrib/sample_fields.json"
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

Since both Bugzilla and JIRA allow field customization, and since it is cumbersome to obtain JIRA custom field metadata dynamically, the Bugjira library will rely on user-supplied configuration information to determine what fields are supported by the user's JIRA and Bugzilla instances. The data Bugjira requires to define fields is specified by the `BugzillaField` and `JiraField` classes in the `bugjira.field` module.

Bugjira obtains its field configuration data from plugins which it loads using [stevedore](https://docs.openstack.org/stevedore/latest/). The plugins are defined in the stevedore `bugjira.field_data.plugins` namespace. The names of the plugins provided with the bugjira source code are referenced in the provided `config/bugjira.json` sample config under the `bugzilla.field_data_plugin_name` and `jira.field_data_plugin_name` attributes. To replace one of the default provided plugins, your plugin should implement the `bugjira.field_data_generator.FieldDataGeneratorInterface` interface and "advertise" itself in the `bugjira.field_data.plugins` namespace, and you should edit bugjira's sample config to indicate the names of the replacement plugins.

The default field data generation plugin class loads data from a file whose path is specified in the config dict under the "field_data_path" key. A sample file is provided in `contrib/sample_fields.json`. The field information in this file is not intended to be comprehensive; if you use the default field data generation plugin, you should edit the sample fields file to support your JIRA and Bugzilla instances and your intended use cases.
