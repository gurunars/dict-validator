import re

from dict_validator import Field


class RegexpField(Field):
    """
    Accept the input that matches a given regular expression.

    :param regexp: string value specifying the regular expression
    :param metavar: a human readable description of what the regexp represents

    >>> from dict_validator import validate, describe

    >>> class Schema:
    ...     field = RegexpField(r"^[ab]{2}$", metavar="TwoCharAOrB")

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
      {'pattern': '^[ab]{2}$',
       'type': 'Regexp(TwoCharAOrB)'})]

    """

    def __init__(self, regexp, metavar=None, *args, **kwargs):
        super(RegexpField, self).__init__(*args, **kwargs)
        self._regexp = re.compile(regexp, re.UNICODE)
        self._metavar = metavar or ""

    def _validate(self, value):
        if not isinstance(value, str):
            return "Not a string"
        if not self._regexp.match(value):
            return "Did not match {}".format(self._type)

    def _describe(self):
        return {
            "pattern": self._regexp.pattern
        }

    @property
    def _type(self):
        return "Regexp({})".format(self._metavar)
