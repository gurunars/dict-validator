import re

from dict_validator import Field


class StringField(Field):
    """
    Match any input of a string type.

    :param regexp: optional string value specifying the regular expression
                   to be used for payload validation
    :param metavar: a human readable description of what the regexp represents

    >>> from dict_validator import validate, describe

    Plain string field

    >>> class Schema:
    ...     field = StringField()

    >>> list(validate(Schema, {"field": "foobar"}))
    []

    >>> list(validate(Schema, {"field": 11}))
    [(['field'], 'Not a string')]

    >>> list(describe(Schema))
    [([], {'type': 'Dict'}), (['field'], {'pattern': None, 'type': 'String'})]

    String field with a regular expression

    >>> class Schema:
    ...     field = StringField(r"^[ab]{2}$", metavar="TwoCharAOrB")

    >>> list(validate(Schema, {"field": "aa"}))
    []

    >>> list(validate(Schema, {"field": "ab"}))
    []

    >>> list(validate(Schema, {"field": "aaa"}))
    [(['field'], 'Did not match Regexp(TwoCharAOrB)')]

    >>> list(validate(Schema, {"field": "cc"}))
    [(['field'], 'Did not match Regexp(TwoCharAOrB)')]

    Serialized payload must be a string

    >>> list(validate(Schema, {"field": 20160710}))
    [(['field'], 'Not a string')]

    >>> from pprint import pprint

    >>> pprint(list(describe(Schema)), width=50)
    [([], {'type': 'Dict'}),
     (['field'],
      {'pattern': '^[ab]{2}$', 'type': 'String'})]

    """

    def __init__(self, regexp=None, metavar=None, *args, **kwargs):
        super(StringField, self).__init__(*args, **kwargs)
        self._regexp = re.compile(regexp, re.UNICODE) if regexp else None
        self._metavar = metavar or ""

    def _validate(self, value):
        if not isinstance(value, str):
            return "Not a string"
        if self._regexp and not self._regexp.match(value):
            return "Did not match Regexp({})".format(self._metavar or
                                                     self._regexp.pattern)

    def _describe(self):
        return {
            "pattern": self._regexp.pattern if self._regexp else None
        }

    @property
    def _type(self):
        return "String"
