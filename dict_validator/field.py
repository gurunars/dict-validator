from abc import ABCMeta, abstractmethod, abstractproperty


class Field(object, metaclass=ABCMeta):
    """
    The "leaf" primitive data type in a schema.
    E.g. string, integer, float, etc.

    :param description: textual explanation of what the field represents
    :param required: True by default. If false - the field is optional

    Each field subclass must implement :attr:`_type` abstract property and
    :meth:`_validate` abstract methods.

    Each field may also implement :meth:`_describe` method.

    Apart from that if custom serialization mechanisms should be in place
    serialize and deserialize methods can be overridden to provide non-default
    behaviour.

    See helper functions for reference implementations of the class.

    .. document private functions
    .. automethod:: _describe
    .. autoattribute:: _type
    .. automethod:: _validate

    """

    def __init__(self, description=None, required=True):
        self._description = description
        self._required = required

    def _describe(self):
        """
        Implement to supply extra info for field's public description.

        :return: **str:%JSON-SERIALIZABLE%** key:value pairs
        :rtype: dict
        """

    @abstractproperty
    def _type(self):
        """
        :return: a human readable string representing a type to be mentioned
                 in the describe method. By default it is a class name.
        :rtype: str
        """

    @abstractmethod
    def _validate(self, value):
        """
        Validate the incoming value, return error message or yield several
        error messages if there are errors.
        """

    # pylint: disable=no-self-use
    def serialize(self, value):
        """
        :return: a payload ready to be sent over the wire
        """
        return value

    # pylint: disable=no-self-use
    def deserialize(self, value):
        """
        :param value: a payload sent over the wire
        :return: a payload with Python specific data types
        """
        return value

    @property
    def required(self):
        """
        Do not override.

        :return: True if the field has to be present in the incoming dict
        """
        return self._required

    def describe(self):
        """
        Do not override.

        :yield: (path, {...description...}),
            e.g (["parent", "child"], {"required": False})
        """
        description = self._describe() or {}
        description["type"] = self._type
        if not self._required:
            description["required"] = False
        if self._description:
            description["description"] = self._description
        yield ([], description)

    def validate(self, value):
        """
        Do not override.

        :param value: a payload
        :yield: (path, erro_msg),
            e.g (["parent", "child"], "Error message")
        """
        result = self._validate(value)

        if result is None:
            return
        elif isinstance(result, str):
            yield ([], result)
        else:
            for chunk in result:
                if isinstance(chunk, (list, tuple)):
                    yield chunk
                else:
                    yield([], chunk)
