from dict_validator.fields import StringField


PART = r"([A-Z]{1}[a-z0-9]+)"
REGEXP = "".join([
    r"^",
    PART,
    r"{1}",
    PART,
    r"*",
    r"$"
])


class PascalCaseField(StringField):
    """
    >>> from dict_validator import validate

    >>> class Schema:
    ...     field = PascalCaseField()

    >>> list(validate(Schema, {"field": 'ValueCapitalized'}))
    []

    Can contain digits

    >>> list(validate(Schema, {"field": 'ValueCapitalizedWith012'}))
    []

    Can't contain non alphanumerics

    >>> list(validate(Schema, {"field": 'Wrong_Value'}))
    [(['field'], 'Did not match Regexp(pascal-case)')]

    Can't start with an int

    >>> list(validate(Schema, {"field": '012WrongValue'}))
    [(['field'], 'Did not match Regexp(pascal-case)')]

    Cant't start with a lowercase

    >>> list(validate(Schema, {"field": 'wrongValue'}))
    [(['field'], 'Did not match Regexp(pascal-case)')]

    Each part should be at least two symbols long (here - 1 - V)

    >>> list(validate(Schema, {"field": 'WrongValueV'}))
    [(['field'], 'Did not match Regexp(pascal-case)')]
    """

    def __init__(self, *args, **kwargs):
        super(PascalCaseField, self).__init__(
            REGEXP,
            "pascal-case", *args, **kwargs)
