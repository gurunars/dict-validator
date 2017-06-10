from dict_validator.fields import StringField


REGEXP = "".join([
    r"^",
    r"([a-z]{1}[a-z0-9]+)",
    r"{1}",
    r"([A-Z]{1}[a-z0-9]+)",
    r"*",
    r"$"
])


class CamelCaseField(StringField):
    """
    >>> from dict_validator import validate

    >>> class Schema:
    ...     field = CamelCaseField()

    >>> list(validate(Schema, {"field": 'value'}))
    []

    Can contain digits

    >>> list(validate(Schema, {"field": 'valueCapitalizedWith012'}))
    []

    Can't contain non alphanumerics

    >>> list(validate(Schema, {"field": 'wrong_Value'}))
    [(['field'], 'Did not match Regexp(camel-case)')]

    Can't start with an int

    >>> list(validate(Schema, {"field": '012wrongValue'}))
    [(['field'], 'Did not match Regexp(camel-case)')]

    Must start with a lowercase

    >>> list(validate(Schema, {"field": 'WrongValue'}))
    [(['field'], 'Did not match Regexp(camel-case)')]

    Each part should be at least two symbols long (here - 1 - V)

    >>> list(validate(Schema, {"field": 'wrongValueV'}))
    [(['field'], 'Did not match Regexp(camel-case)')]

    Even the first part should contain at least two symbols

    >>> list(validate(Schema, {"field": 'wRongValueV'}))
    [(['field'], 'Did not match Regexp(camel-case)')]
    """

    def __init__(self, *args, **kwargs):
        super(CamelCaseField, self).__init__(
            REGEXP,
            "camel-case", *args, **kwargs)
