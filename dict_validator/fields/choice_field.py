from dict_validator import Field


class Choice(Field):
    """
    Accept any type of input as long as it matches on of the choices
    mentioned in the provided list.

    :param choices: list of choices to match against

    >>> from dict_validator import validate, describe

    >>> class Schema:
    ...     field = Choice(choices=["ONE", "TWO", 3, 4])

    >>> list(validate(Schema, {"field": "ONE"}))
    []

    >>> list(validate(Schema, {"field": 4}))
    []

    >>> list(validate(Schema, {"field": "4"}))
    [(['field'], 'Not among the choices')]

    >>> list(validate(Schema, {"field": 1}))
    [(['field'], 'Not among the choices')]

    >>> list(validate(Schema, {"field": "FOUR"}))
    [(['field'], 'Not among the choices')]

    >>> from pprint import pprint

    >>> pprint(list(describe(Schema)))
    [([], {'type': 'Dict'}),
     (['field'], {'choices': ['ONE', 'TWO', 3, 4], 'type': 'Choice'})]

    """

    def __init__(self, choices, *args, **kwargs):
        super(Choice, self).__init__(*args, **kwargs)
        self._choices = choices

    def _validate(self, value):
        if value not in self._choices:
            return "Not among the choices"

    def _describe(self):
        return {
            "choices": self._choices
        }
