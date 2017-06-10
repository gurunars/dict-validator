from dict_validator.fields import StringField


REGEXP = "".join([
    r"^",
    r"([a-z]{1}[a-z0-9]+)",
    r"{1}",
    r"(_{1}[a-z0-9]{1}[a-z0-9]+)",
    r"*",
    r"$"
])


class UnderscoreCaseField(StringField):
    """
    >>> from dict_validator import validate

    >>> class Schema:
    ...     field = UnderscoreCaseField()

    >>> list(validate(Schema, {"field": 'value'}))
    []

    >>> list(validate(Schema, {"field": 'value_with_parts'}))
    []

    Can contain digits

    >>> list(validate(Schema, {"field": 'value_with_12'}))
    []

    Can't contain upper case chars

    >>> list(validate(Schema, {"field": 'wrong_Value'}))
    [(['field'], 'Did not match Regexp(underscore-case)')]

    Can't start with an int

    >>> list(validate(Schema, {"field": '012wrong_value'}))
    [(['field'], 'Did not match Regexp(underscore-case)')]

    Can't start with an underscore

    >>> list(validate(Schema, {"field": '_wrong_value'}))
    [(['field'], 'Did not match Regexp(underscore-case)')]

    Can't end with an underscore

    >>> list(validate(Schema, {"field": 'wrong_value_'}))
    [(['field'], 'Did not match Regexp(underscore-case)')]

    Each part should be at least two symbols long (here - 1 - V)

    >>> list(validate(Schema, {"field": 'wrong_v'}))
    [(['field'], 'Did not match Regexp(underscore-case)')]

    Even the first part should contain at least two symbols

    >>> list(validate(Schema, {"field": 'w_rong_value'}))
    [(['field'], 'Did not match Regexp(underscore-case)')]
    """

    def __init__(self, *args, **kwargs):
        super(UnderscoreCaseField, self).__init__(
            REGEXP,
            "underscore-case", *args, **kwargs)
