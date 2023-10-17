class BrokerException(Exception):
    pass


class BrokerInitException(BrokerException):
    pass


class BrokerAddCommentException(BrokerException):
    pass


class BrokerLookupException(BrokerException):
    pass


class FieldDataGeneratorException(Exception):
    pass


class PluginLoaderException(Exception):
    pass
