class BrokerException(Exception):
    pass


class BrokerInitException(BrokerException):
    pass


class BrokerAddCommentException(BrokerException):
    pass


class BrokerLookupException(BrokerException):
    pass


class JsonGeneratorException(Exception):
    pass


class PluginLoaderException(Exception):
    pass
