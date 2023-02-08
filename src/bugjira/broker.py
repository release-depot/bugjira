from bugzilla import Bugzilla
from jira import JIRA

from bugjira.config import Config
from bugjira.issue import BugzillaIssue, Issue, JiraIssue


class Broker:
    def __init__(self, config=None, backend=None) -> None:
        """Init method for the Broker class

        :param config: An optional config dict, defaults to None
        :type config: dict, optional
        :param backend: An optional API backend instance, defaults to None
        :type backend: object, optional
        :raises BrokerInitException: If neither a config nor a backend is
            provided
        """
        if config is None and backend is None:
            raise BrokerInitException("API backend or config dict required")
        self.backend = backend

    def get_issue(self, key) -> Issue:
        # Override in subclasses
        pass


class BugzillaBroker(Broker):
    """A Broker for interacting with bugzilla"""

    def __init__(self, config=None, backend=None) -> None:
        """Init method for the BugzillaBroker class

        :param config: A dict containing config information for the bugzilla
            backend, defaults to None
        :type config: dict, optional
        :param backend: A pre-initialized bugzilla api backend object, defaults
            to None
        :type backend: bugzilla.Bugzilla, optional
        """
        super().__init__(config, backend)
        if self.backend is None:
            config = Config.from_config(config_dict=config)
            url = config.get("bugzilla").get("URL")
            api_key = config.get("bugzilla").get("api_key")
            self.backend = Bugzilla(url, api_key=api_key)

    def get_issue(self, key) -> BugzillaIssue:
        """Return an Issue that wraps a bugzilla bug returned by the backend

        :param key: A bugzilla bug id to lookup in bugzilla
        :type key: str
        :raises BrokerLookupException: if an Exception occurs when using the
            backend's getbug method
        :return: A BugzillaIssue that wraps a bugzilla bug
        :rtype: BugzillaIssue
        """
        try:
            bug = self.backend.getbug(key)
        except Exception as e:
            raise BrokerLookupException(e)
        return BugzillaIssue(key=key, bugzilla=bug)


class JiraBroker(Broker):
    """A Broker for interacting with JIRA"""

    def __init__(self, config=None, backend=None) -> None:
        """Init method for the JiraBroker class

        :param config: A dict containing config information for the Jira
            backend, defaults to None
        :type config: dict, optional
        :param backend: A pre-initialized Jira api backend object, defaults to
            None
        :type backend: jira.JIRA, optional
        """
        super().__init__(config, backend)
        if self.backend is None:
            config = Config.from_config(config_dict=config)
            url = config.get("jira").get("URL")
            token_auth = config.get("jira").get("token_auth")
            self.backend = JIRA(url, token_auth=token_auth)

    def get_issue(self, key) -> JiraIssue:
        """Return an Issue that wraps a JIRA issue returned by the backend

        :param key: A jira issue key to lookup in jira
        :type key: str
        :raises BrokerLookupException: if an Exception occurs when using the
            backend's issue method
        :return: A JiraIssue that wraps a JIRA issue
        :rtype: JiraIssue
        """
        try:
            issue = self.backend.issue(key)
        except Exception as e:
            raise BrokerLookupException(e)
        return JiraIssue(key=key, jira_issue=issue)


class BrokerException(Exception):
    pass


class BrokerInitException(BrokerException):
    pass


class BrokerLookupException(BrokerException):
    pass
