from bugjira.common import BUGZILLA, JIRA
from bugjira.field import BugjiraField, BugzillaField, JiraField
from bugjira.field_data_generator import factory \
    as field_data_generator_factory


class FieldGenerator:
    """Instances of this class obtain a FieldDataGenerator from the
    field_data_generator_factory, and they use the raw field data from
    the FieldDataGenerator to return a list of BugjiraField objects via the
    get_fields method.
    """

    def __init__(self, generator_type, config):
        """Init method

        :param generator_type: The generator type for this FieldGenerator
        :type generator_type: str
        :param config: a valid Bugjira config dict
        :type config: dict
        """
        self.config = config
        self.field_data_generator = field_data_generator_factory\
            .get_field_data_generator(generator_type, config)
        self.field_class = self._get_field_class(generator_type)

    def _field_data_to_class(self, field_data) -> [BugjiraField]:
        """Returns a list of BugjiraField objects that correspond to the
        generator type used to instantiate the class

        :param field_data: A list of dicts representing data that can be used
            to instantiate BugjiraField subclasses
        :type field_data: [dict]
        :return: A list of BugjiraField instances
        :rtype: [BugjiraField]
        """
        return [self.field_class(**data) for data in field_data]

    def _get_field_class(self, generator_type) -> BugjiraField:
        """Given a generator type, return the BugjiraField subclass that
        corresponds to the generator type.

        :param generator_type: A valid generator type
        :type generator_type: str
        :raises ValueError: Raised if an invalid generator type is passed in
        :return: The BugjiraField subclass corresponding to the generator type
        :rtype: BugjiraField
        """
        if generator_type == BUGZILLA:
            return BugzillaField
        elif generator_type == JIRA:
            return JiraField
        else:
            raise ValueError(generator_type)

    def get_fields(self) -> [BugjiraField]:
        """Get the data for instantiating BugzillaField or JiraField objects
        from the field_data_generator plugin's get_field_data method and then
        use the _field_data_to_class method to return a list of instances.

        :return: a list of instances whose superclass is BugjiraField
        :rtype: [BugjiraField]
        """
        field_data = self.field_data_generator.get_field_data()
        return self._field_data_to_class(field_data)


class FieldGeneratorFactory:
    """Factory class that returns the FieldGenerator associated with the input
    generator_type.
    """
    def __init__(self):
        self._generators = {}

    def get_field_generator(self, generator_type, config) -> FieldGenerator:
        """Return the FieldGenerator associated with the generator_type.
        Instantiate the FieldGenerator first if it is not already in the
        factory's _generators dict under the generator_type key.

        :param generator_type: The desired field generator type
        :type generator_type: str
        :param config: A valid bugjira config dict
        :type config: dict
        :return: The FieldGenerator corresponding to the generator type
        :rtype: FieldGenerator
        """
        generator = self._generators.get(generator_type, None)
        if not generator:
            generator = FieldGenerator(generator_type, config)
            self._generators[generator_type] = generator
        return generator


factory = FieldGeneratorFactory()
