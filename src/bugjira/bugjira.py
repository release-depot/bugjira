from bugjira.broker import BugzillaBroker, JiraBroker
from bugjira.config import Config
from bugjira.issue import Issue
from bugjira.util import is_bugzilla_key, is_jira_key


class Bugjira:
    """API abstraction layer object for a bugzilla backend and a jira
    backend."""

    def __init__(
        self, config_path="", config_dict=None, bugzilla=None, jira=None
    ):
        """Init method for the Bugjira class. Note that if both config_dict and
        config_path parameters are provided, the config_dict will take
        precedence.

        :param config_path: Absolute path to a json config file, defaults to ""
        :type config_path: str, optional
        :param config_dict: A dict containing configuration info for Bugzilla
            and Jira instances
        :type config_dict: dict, optional
        :param bugzilla: An already-initialized bugzilla.Bugzilla instance,
            defaults to None
        :type bugzilla: bugzilla.Bugzilla, optional
        :param jira: An already-initialized jira.JIRA instance, defaults to
            None
        :type jira: jira.JIRA, optional
        """
        self.config = None
        if config_dict:
            self.config = Config.from_config(config_dict=config_dict)
        elif config_path:
            self.config = Config.from_config(config_path=config_path)

        self._bugzilla_broker = BugzillaBroker(
            config=self.config, backend=bugzilla
        )
        self.bugzilla = self._bugzilla_broker.backend

        self._jira_broker = JiraBroker(config=self.config, backend=jira)
        self.jira = self._jira_broker.backend

    def get_issue(self, key) -> Issue:
        """Return an Issue using the correct Broker based on the key input

        :param key: The lookup key
        :type key: str
        :return: A bugjira Issue that wraps the bugzilla or jira returned by
            the broker
        :rtype: Issue
        """
        if not isinstance(key, str):
            raise ValueError(f"key must be a string: {key}")
        broker = self._get_broker(key)
        return broker.get_issue(key)

    def _get_broker(self, key):
        """Private method to return the correct backend Broker based on the
        input key.

        :param key: Either a bugzilla bug id or a Jira issue key
        :type key: str
        :raises ValueError: If the input key is not a bugzilla id or a jira
            issue key
        :return: The correct Broker to handle operations on the Issue
        :rtype: bugjira.broker.Broker
        """
        if is_bugzilla_key(key):
            return self._bugzilla_broker

        if is_jira_key(key):
            return self._jira_broker

        raise ValueError("key does not appear to be bugzilla or jira ID")
