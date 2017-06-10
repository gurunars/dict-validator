import datetime

from dict_validator import Field


def _datetime(value):
    """Return datetime object."""
    return value


class TimestampField(Field):
    """
    UTC timestamp. Could be a datetime, a date or time. By default it is
    datetime.

    The timestamp has to be formatted according to:
    https://en.wikipedia.org/wiki/ISO_8601

    The incoming string is deserialized into datetime object.
    The outgoing datetime object is serialized into a string.

    :param granularity: one of
        [TimestampField.DateTime, TimestampField.Date, TimestampField.Time]

    >>> from argparse import Namespace
    >>> from pprint import pprint

    >>> from dict_validator import validate, describe, deserialize, serialize

    By default a DateTime is expected.

    >>> class Schema:
    ...     field = TimestampField()

    >>> pprint(list(describe(Schema)))
    [([], {'type': 'Dict'}),
     (['field'], {'granularity': 'DateTime', 'type': 'Timestamp'})]

    >>> list(validate(Schema, {"field": '2016-07-10 13:06:04.698084'}))
    []

    >>> list(validate(Schema, {"field": '2016-07-10'}))
    [(['field'], 'Not a valid DateTime')]

    >>> deserialize(Schema, {"field": "2016-07-10 13:06:04.698084"}).field
    datetime.datetime(2016, 7, 10, 13, 6, 4, 698084)

    >>> serialize(Schema, Namespace(
    ...     field=datetime.datetime(2016, 7, 10, 13, 6, 4, 698084)
    ... ))
    {'field': '2016-07-10 13:06:04.698084'}

    Accept Date only.

    >>> class Schema:
    ...     field = TimestampField(granularity=TimestampField.Date)

    >>> pprint(list(describe(Schema)))
    [([], {'type': 'Dict'}),
     (['field'], {'granularity': 'Date', 'type': 'Timestamp'})]

    >>> list(validate(Schema, {"field": '2016-07-10'}))
    []

    Serialized payload must be a string

    >>> list(validate(Schema, {"field": 20160710}))
    [(['field'], 'Not a string')]

    >>> deserialize(Schema, {"field": "2016-07-10"}).field
    datetime.date(2016, 7, 10)

    >>> serialize(Schema, Namespace(
    ...     field=datetime.date(2016, 7, 10)
    ... ))
    {'field': '2016-07-10'}

    Accept Time only.

    >>> class Schema:
    ...     field = TimestampField(granularity=TimestampField.Time)

    >>> pprint(list(describe(Schema)))
    [([], {'type': 'Dict'}),
     (['field'], {'granularity': 'Time', 'type': 'Timestamp'})]

    >>> list(validate(Schema, {"field": '13:06:04.698084'}))
    []

    >>> deserialize(Schema, {"field": "13:06:04.698084"}).field
    datetime.time(13, 6, 4, 698084)

    >>> serialize(Schema, Namespace(
    ...     field=datetime.time(13, 6, 4, 698084)
    ... ))
    {'field': '13:06:04.698084'}

    """

    # pylint: disable=missing-docstring, no-init, too-few-public-methods

    class DateTime(object):
        value = "%Y-%m-%d %H:%M:%S.%f"
        granulate = staticmethod(_datetime)

    class Date(object):
        value = "%Y-%m-%d"
        granulate = datetime.datetime.date

    class Time(object):
        value = "%H:%M:%S.%f"
        granulate = datetime.datetime.time

    def __init__(self, granularity=DateTime, *args, **kwargs):
        super(TimestampField, self).__init__(*args, **kwargs)
        self._granularity = granularity

    def _validate(self, value):
        if not isinstance(value, str):
            return "Not a string"
        try:
            datetime.datetime.strptime(value, self._granularity.value)
        except ValueError:
            return "Not a valid {}".format(self._granularity.__name__)

    def deserialize(self, value):
        now = datetime.datetime.strptime(value, self._granularity.value)
        return self._granularity.granulate(now)

    def serialize(self, value):
        return value.strftime(self._granularity.value)

    @property
    def _type(self):
        return "Timestamp"

    def _describe(self):
        return {
            "granularity": self._granularity.__name__
        }
