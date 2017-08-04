from dict_validator.fields import String


class Phone(String):
    """
    Make sure that the input is a valid phone number.

    >>> from dict_validator import validate, deserialize

    >>> class Schema:
    ...     field = Phone()

    >>> list(validate(Schema, {"field": '+358 807 12'}))
    []

    Has to start with a +

    >>> list(validate(Schema, {"field": '358 807 12'}))
    [(['field'], 'Did not match Regexp(phone)')]

    >>> deserialize(Schema, {"field": '+358 807 12'}).field
    '+35880712'

    """

    def __init__(self, *args, **kwargs):
        super(Phone, self).__init__(
            r"^\+[0-9]{1,4}[ 0-9]+$", "phone",
            *args, **kwargs)

    def deserialize(self, value):
        return value.replace(" ", "")
