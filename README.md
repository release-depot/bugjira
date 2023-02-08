# Bugjira
Bugjira is an abstraction layer library for interacting with either bugzilla or JIRA via their respective python libraries.

## Examples

Bugjira users can perform common operations (lookup, query, modify, etc) on both bugs (bugzilla) and issues (jira) using the Bugjira object.

Configuration is provided with either a dict (see below) or a pathname to a config file containing a json dict (a sample config file is included in `contrib/bugjira.json`):

```python
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
