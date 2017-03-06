from dict_validator import Field


class AnyField(Field):

    @property
    def _type(self):
        return "AnyValue"

    def _validate(self, value):
        pass


class WildcardDictField(Field):
    """
    Match a dict with any dict with any key/value pairs.

    :param key_schema: Field subclass to be used to
        validate/serialize/deserialize the keys. Optional. If undefined the
        keys are accepted as is.
    :param value_schema: Field subclass to be used to
        validate/serialize/deserialize the values. Optional. If undefined the
        values are accepted as is.

    >>> from dict_validator import validate, describe, serialize, deserialize

    >>> class Schema:
    ...     field = WildcardDictField()

    >>> list(validate(Schema, {"field": {}}))
    []

    >>> list(validate(Schema, {"field": {"key": "value"}}))
    []

    >>> list(validate(Schema, {"field": 11}))
    [(['field'], 'Not a dict')]

    >>> from pprint import pprint

    In field's description there are two special nodes: *{KEY}* and *{VALUE}*
    that respectively correspond to the schemas applied to keys and values of
    the payload.

    >>> pprint(list(describe(Schema)), width=70)
    [([], {'type': 'Dict'}),
     (['field'], {'type': 'WildcardDict'}),
     (['field', '{KEY}'], {'type': 'AnyValue'}),
     (['field', '{VALUE}'], {'type': 'AnyValue'})]

    If it is need it is possible to have validation for keys, values or both.
    This can be achieved by defining respective schemas.

    >>> class SampleOnlyField(Field):
    ...
    ...     @property
    ...     def _type(self):
    ...         return "SampleOnly"
    ...
    ...     def _validate(self, value):
    ...         if not value.startswith("sample"):
    ...             return "Not a sample"
    ...
    ...     def serialize(self, value):
    ...         return value.lstrip("py(").rstrip(")")
    ...
    ...     def deserialize(self, value):
    ...         return "py(" +  value + ")"

    >>> class Schema:
    ...     field = WildcardDictField(key_schema=SampleOnlyField(),
    ...                               value_schema=SampleOnlyField())

    >>> pprint(list(describe(Schema)), width=70)
    [([], {'type': 'Dict'}),
     (['field'], {'type': 'WildcardDict'}),
     (['field', '{KEY}'], {'type': 'SampleOnly'}),
     (['field', '{VALUE}'], {'type': 'SampleOnly'})]

    >>> list(validate(Schema, {"field": {
    ...     "sample_field": "sample_value"
    ... }}))
    []

    >>> list(validate(Schema, {"field": {
    ...     "foobar": "sample_value"
    ... }}))
    [(['field', 'foobar'], 'Key error: Not a sample')]

    >>> list(validate(Schema, {"field": {
    ...     "sample_field": "foobar"
    ... }}))
    [(['field', 'sample_field'], 'Value error: Not a sample')]

    >>> from argparse import Namespace

    >>> serialize(Schema, Namespace(
    ...     field={"py(foobar)": "py(sample_value)"}
    ... ))
    {'field': {'foobar': 'sample_value'}}

    >>> deserialize(Schema, {"field": {"foobar": "sample_value"}}).field
    {'py(foobar)': 'py(sample_value)'}

    """

    def __init__(self, key_schema=None, value_schema=None, *args, **kwargs):
        super(WildcardDictField, self).__init__(*args, **kwargs)
        self._key_schema = key_schema or AnyField()
        self._value_schema = value_schema or AnyField()

    def describe(self):
        for result in super(WildcardDictField, self).describe():
            yield result
        for (child_path, description) in self._key_schema.describe():
            yield (['{KEY}'] + child_path, description)
        for (child_path, description) in self._value_schema.describe():
            yield (['{VALUE}'] + child_path, description)

    @property
    def _type(self):
        return "WildcardDict"

    def _validate(self, value):
        if not isinstance(value, dict):
            yield "Not a dict"
            return
        for key, payload in value.items():
            for (child_path, error) in self._key_schema.validate(key):
                yield ([key] + child_path, "Key error: " + error)
            for (child_path, error) in self._value_schema.validate(payload):
                yield ([key] + child_path, "Value error: " + error)

    def serialize(self, value):
        ret_val = {}
        for key, val in value.items():
            ret_val[self._key_schema.serialize(key)] = \
                self._value_schema.serialize(val)
        return ret_val

    def deserialize(self, value):
        ret_val = {}
        for key, val in value.items():
            ret_val[self._key_schema.deserialize(key)] = \
                self._value_schema.deserialize(val)
        return ret_val
