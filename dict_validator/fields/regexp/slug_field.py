from dict_validator.fields import StringField


class SlugField(StringField):
    """
    Lower case alphanumerics delimited with dashes.

    >>> from dict_validator import validate

    >>> class Schema:
    ...     field = SlugField()

    >>> list(validate(Schema, {"field": 'title-of-web-page'}))
    []

    Too many dashes

    >>> list(validate(Schema, {"field": 'title--of-web-page'}))
    [(['field'], 'Did not match Regexp(slug)')]

    Starts with a dash

    >>> list(validate(Schema, {"field": '-title-of-web-page'}))
    [(['field'], 'Did not match Regexp(slug)')]

    Ends with a dash

    >>> list(validate(Schema, {"field": 'title-of-web-page-'}))
    [(['field'], 'Did not match Regexp(slug)')]

    """

    def __init__(self, *args, **kwargs):
        super(SlugField, self).__init__(
            r"^[a-z0-9]+(-[a-z0-9]+)*$",
            "slug", *args, **kwargs)
