import re


def is_bugzilla_key(key):
    """returns True if the input key is in the format of a bugzilla bug ID

    :param key: The input key to test
    :type key: str
    :raises ValueError: If the key is not of type str
    :return: True if the input key is in the format of a bugzilla bug ID
    :rtype: bool
    """
    if not isinstance(key, str):
        raise ValueError(f"Key must be a str: {key}")
    bz = re.compile("^[0-9]+$")
    if bz.match(key):
        return True
    return False


def is_jira_key(key):
    """returns True if the input key is in the format of a JIRA issue key

    :param key: The input key to test
    :type key: str
    :raises ValueError: If the key is not of type str
    :return: True if the input key is in the format of a JIRA issue key
    :rtype: bool
    """
    if not isinstance(key, str):
        raise ValueError(f"Key must be a str: {key}")
    jira = re.compile("[a-zA-Z]+[-_][0-9]+")
    if jira.match(key):
        return True
    return False
