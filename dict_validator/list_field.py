""" dict_validator.list_field """

from .field import Field


class ListField(Field):
    """
    A collection of arbitrary items.

    :param schema: Field subclass to be used to validate/serialize individual
        items of the collection
    """

    def __init__(self, schema, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
        self._schema = schema

    def _validate(self, value):
        if not isinstance(value, list):
            yield ([], "Not a list")
            return
        count = 0
        for item in value:
            for (child_path, error) in self._schema.validate(item):
                yield ([count] + child_path, error)
            count += 1

    def describe(self):
        for result in super(ListField, self).describe():
            yield result
        for (child_path, description) in self._schema.describe():
            yield (['{N}'] + child_path, description)

    def serialize(self, value):
        return [self._schema.serialize(val) for val in value]

    def deserialize(self, value):
        return [self._schema.deserialize(val) for val in value]
