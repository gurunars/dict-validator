"""
The package aims to simplify payload validation using schemas represented by
by regular Python classes.

In the heart of the library there are just a few top level concepts.

To begin with a Schema is nothing else but a collection of fields
that boils down to a definition of the following shape:

.. code:: python

    class Schema:
        field1 = Sample()  # this a field
        field2 = Other()  # and this is a field

Where each field is a subclass of a :class:`Field` with zero or more
constructor parameters.

Note, you may extend an "object" but it is truly optional.

Once a schema is defined it is possible to employ one of the functions to
process the payload and/or schema:

 - :func:`validate` - to check the payload
 - :func:`serialize_errors` - to to transform :func:`validate` results into a
   flat dict that could be sent over the wire
 - :func:`describe` - to present the schema in a serializable format
 - :func:`serialize` - to transform the payload with Python specific types
   into something that could be sent over the wire
 - :func:`deserialize` - reverse of :func:`serialize`

Most common Field subclasses can be found in :mod:`dict_validator.fields`.

"""

from .helpers import validate, describe, serialize, deserialize, \
    serialize_errors
from .field import Field
from .list_field import List
from .dict_field import Dict

__all__ = ["validate", "describe", "serialize", "deserialize", "Field",
           "Dict", "List", "serialize_errors"]
