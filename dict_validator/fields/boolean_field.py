from dict_validator import Field


class Boolean(Field):
    """
    Match a boolean.

    >>> from dict_validator import validate, describe

    >>> class Schema:
    ...     field = Boolean()

    >>> list(validate(Schema, {"field": True}))
    []

    >>> list(validate(Schema, {"field": 11}))
    [(['field'], 'Not a boolean')]

    >>> list(describe(Schema))
    [([], {'type': 'Dict'}), (['field'], {'type': 'Boolean'})]

    """

    def _validate(self, value):
        if not isinstance(value, bool):
            return "Not a boolean"
