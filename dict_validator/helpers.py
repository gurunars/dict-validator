from collections import defaultdict

from .dict_field import DictField


def _wrap_schema(schema):
    if isinstance(schema, type):
        return DictField(description=schema.__doc__, schema=schema)
    return schema


def validate(schema, value):
    """
    Validate value again a given schema.

    :param schema: a class representing the structure to be used for validation
    :param value: a dict
    :yield: (path, erro_msg),
        e.g (["parent", "child"], "Error message")

    >>> from dict_validator import Field, ListField, DictField

    To report a single error _validate method of a field subclass must
    return a string description of the problem.

    >>> class SampleOnlyField(Field):
    ...
    ...     @property
    ...     def _type(self):
    ...         return "NOT IMPORTANT"
    ...
    ...     def _validate(self, value):
    ...         if value != "sample":
    ...             return "Not a sample"

    >>> class Schema:
    ...     field = SampleOnlyField()

    If there are no problems - nothing is yielded.
    Note: validate function is a generator - thus it has to be converted
    to a list explicitly.

    >>> list(validate(Schema, {"field": "sample"}))
    []

    Payload must be a dict.

    >>> list(validate(Schema, "NOT A DICT"))
    [([], 'Not a dict')]

    If there are problems - a collection of tuples is yielded.
    The first element of a tuple is a list representing an absolute path
    to the field.
    The second element is a string with a description of the problem.

    >>> list(validate(Schema, {"field": "not sample"}))
    [(['field'], 'Not a sample')]

    By default all fields are required

    >>> list(validate(Schema, {}))
    [([], 'Key "field" is missing')]

    By design no extra fields are allowed - payload must be strictly specified.

    >>> list(validate(Schema, {"field": "sample", "unknown_field": "sample"}))
    [([], 'Unkown fields: unknown_field')]

    Optional fields are marked via required=False parameter.
    This parameter is available for any field and its behaviour is uniform.

    >>> class Schema:
    ...     field = SampleOnlyField(required=False)

    >>> list(validate(Schema, {"field": "sample"}))
    []

    >>> list(validate(Schema, {"field": "not sample"}))
    [(['field'], 'Not a sample')]

    If optional field is missing - no error is reported.

    >>> list(validate(Schema, {}))
    []

    Alternative way to report errors is to yield them.
    It is a good idea if there is a need to validate multiple aspects
    of the input value.

    >>> class WithYieldedErrorField(Field):
    ...
    ...     @property
    ...     def _type(self):
    ...         return "NOT IMPORTANT"
    ...
    ...     def _validate(self, value):
    ...         yield "Error 1"
    ...         yield "Error 2"

    >>> class Schema:
    ...     field = WithYieldedErrorField()

    Each error has its own unique error tuple even if the errors originate
    from the same field.

    >>> list(validate(Schema, {"field": "sample"}))
    [(['field'], 'Error 1'), (['field'], 'Error 2')]

    Nested structures can be described using a DictField.
    This field requires a reference to the schema specifying a nested
    structure.

    >>> class Child:
    ...     other_field = SampleOnlyField()

    >>> class Parent:
    ...     child = DictField(Child)

    >>> list(validate(Parent, {"child": {"other_field": "sample"}}))
    []

    The absolute path to the error includes all the nodes of the structure's
    tree.

    >>> list(validate(Parent, {"child": {"other_field": "not sample"}}))
    [(['child', 'other_field'], 'Not a sample')]

    To represent collections of data (aka lists) a ListField should be used.
    The field requires an instance of some other field as its first argument.

    >>> class Schema:
    ...     field = ListField(SampleOnlyField())

    >>> list(validate(Schema, {"field": "NOT A LIST"}))
    [(['field'], 'Not a list')]

    >>> list(validate(Schema, {"field": ["sample"]}))
    []

    If the problem is in individual item a path to the node includes
    an integer index of the node.

    >>> list(validate(Schema, {"field": ["not sample", "sample",
    ...                                  "not sample"]}))
    [(['field', 0], 'Not a sample'), (['field', 2], 'Not a sample')]

    It is possible to have a sophisticated nesting using a combination of
    list and dict fields.

    >>> class Child:
    ...     other_field = SampleOnlyField()

    >>> class Parent:
    ...     child = ListField(DictField(Child))

    >>> list(validate(Parent, {"child": [{"other_field": "sample"}]}))
    []

    >>> list(validate(Parent, {"child": [{"other_field": "not sample"}]}))
    [(['child', 0, 'other_field'], 'Not a sample')]

    """
    return _wrap_schema(schema).validate(value)


def serialize_errors(validation_results):
    """
    Transform a denormalized generator over the collection of errors
    into a serializable normalized dict.

    :param validation_generator: a collection of errors returned by
                                 :func:`validate`
    :return: dict with field paths as keys and lists of errors
             corresponding to those paths as values

    >>> error_collection = iter([
    ...     (['field', 0], 'Error #1'),
    ...     (['field', 2], 'Error #1'),
    ...     (['field', 2], 'Error #2')
    ... ])

    >>> from pprint import pprint

    >>> pprint(serialize_errors(error_collection))
    {'field.0': ['Error #1'], 'field.2': ['Error #1', 'Error #2']}
    """
    return_value = defaultdict(list)
    for path, error in validation_results:
        return_value[".".join(map(str, path))].append(error)
    return dict(return_value)


def describe(schema):
    """
    Describe a given schema.

    Understands primitive, list and dict fields.

    :param schema: a class representing the structure to be documented
    :yield: (path, {...description...}),
        e.g (["parent", "child"], {"required": False})

    >>> from dict_validator import Field, ListField, DictField

    Each custom field must be a Field subclass with _type property
    and _validate method implemented.

    See validate function for details.

    >>> class AnyValue(Field):
    ...
    ...     @property
    ...     def _type(self):
    ...         return "AnyValue"
    ...
    ...     def _validate(self, value):
    ...         pass

    To document a field - pass a "description" parameter to the constructor.
    The value must be a string.
    The "description" can be added to any field.

    >>> class Child:
    ...     items = ListField(AnyValue("AnyValue item"),
    ...                       description="A collection of important items")

    >>> class Parent:
    ...     '''Schema docstring'''
    ...
    ...     ignored_field = "Nothing"
    ...     child = DictField(Child, description="Dict child")
    ...     plain_field = AnyValue(description="Pure string", required=False)

    Since return value is a generator it has to be explicitly converted to
    a list.

    Note, when it comes to documenting the items of the list "{N}" string
    is used to denote such a field.

    Also note that a docstring of the schema class is transformed into
    a description of the top-level schema.

    >>> from pprint import pprint

    >>> pprint(sorted(describe(Parent)), width=60)
    [([], {'description': 'Schema docstring', 'type': 'Dict'}),
     (['child'], {'description': 'Dict child', 'type': 'Dict'}),
     (['child', 'items'],
      {'description': 'A collection of important items',
       'type': 'List'}),
     (['child', 'items', '{N}'],
      {'description': 'AnyValue item', 'type': 'AnyValue'}),
     (['plain_field'],
      {'description': 'Pure string',
       'required': False,
       'type': 'AnyValue'})]
    """
    return _wrap_schema(schema).describe()


def serialize(schema, value):
    """
    Serialize a value before sending it over the wire.

    Understands primitive, list and dict fields.

    :param schema: a class representing the structure to be used for
        serialization
    :param value: a pythonic object
    :return: a dict ready to be sent over the wire

    >>> from dict_validator import Field, ListField, DictField, serialize

    Each custom field must be a Field should implement a serialize method
    to enable value transformations by default the value is returned as is.

    See Field docs for details

    >>> class AnyValueField(Field):
    ...
    ...     @property
    ...     def _type(self):
    ...         return "NOT IMPORTANT"
    ...
    ...     def _validate(self, value):
    ...         pass
    ...
    ...     def serialize(self, value):
    ...         return "SERIALIZED {}".format(super(AnyValueField, self)
    ...             .serialize(value))

    >>> class Child:
    ...     items = ListField(AnyValueField("String item"),
    ...                       description="A collection of important items")

    >>> class Parent:
    ...     child = DictField(Child, description="Dict child")
    ...     plain_field = AnyValueField(description="Pure string",
    ...                                 required=False)

    In order to construct a tree of python objects to serialize it later one
    just use a Namespace class from the standard library.

    >>> from argparse import Namespace

    >>> payload = Namespace(
    ...     plain_field="OUTGOING",
    ...     child=Namespace(
    ...         items=["OUTGOING"]
    ...     )
    ... )

    >>> from pprint import pprint

    >>> pprint(serialize(Parent, payload))
    {'child': {'items': ['SERIALIZED OUTGOING']},
     'plain_field': 'SERIALIZED OUTGOING'}

    When serializing optional fields the missing values are set to None.

    >>> class Schema:
    ...     field = AnyValueField(required=False)

    >>> serialize(Schema, {})
    {'field': None}

    """
    return _wrap_schema(schema).serialize(value)


def deserialize(schema, value):
    """
    Deserialize a value after sending it over the wire into a pythonic object.

    Understands primitive, list and dict fields.

    :param schema: a class representing the structure to be used for
        deserialization
    :param value: a dict sent over the wire
    :return: a pythonic object

    >>> from dict_validator import Field, ListField, DictField, deserialize

    Each custom field must be a Field should implement a deserialize method
    to enable value transformations by default the value is returned as is.

    See Field docs for details

    >>> class AnyValueField(Field):
    ...
    ...     @property
    ...     def _type(self):
    ...         return "NOT IMPORTANT"
    ...
    ...     def _validate(self, value):
    ...         pass
    ...
    ...     def deserialize(self, value):
    ...         return "DESERIALIZED {}".format(super(AnyValueField, self)
    ...             .deserialize(value))

    >>> class Child:
    ...     items = ListField(AnyValueField("String item"),
    ...                       description="A collection of important items")

    >>> class Parent:
    ...     child = DictField(Child, description="Dict child")
    ...     plain_field = AnyValueField(description="Pure string",
    ...                                 required=False)

    >>> parent = deserialize(Parent, {
    ...     "child": {
    ...         "items": ["INCOMING"]
    ...     },
    ...     "plain_field": "INCOMING"
    ... })

    >>> parent.plain_field
    'DESERIALIZED INCOMING'

    >>> parent.child.items[0]
    'DESERIALIZED INCOMING'

    When deserializing optional fields the missing values are set to None.

    >>> class Schema:
    ...     field = AnyValueField(required=False)

    >>> deserialize(Schema, {}).field

    """
    return _wrap_schema(schema).deserialize(value)
