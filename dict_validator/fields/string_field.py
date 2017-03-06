from dict_validator import Field


class StringField(Field):
    """
    Match any input of string type.

    >>> from dict_validator import validate, describe

    >>> class Schema:
    ...     field = StringField()

    >>> list(validate(Schema, {"field": "foobar"}))
    []

    >>> list(validate(Schema, {"field": 11}))
    [(['field'], 'Not a string')]

    >>> list(describe(Schema))
    [([], {'type': 'Dict'}), (['field'], {'type': 'String'})]

    """

    @property
    def _type(self):
        return "String"

    def _validate(self, value):
        if not isinstance(value, str):
            return "Not a string"
