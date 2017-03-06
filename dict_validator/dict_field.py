from .field import Field


class DictField(Field):
    """
    A dict of values.

    :param schema: class to be used for validation/serialization of the
        incoming values
    :type schema: dict_validator.Schema
    """

    def __init__(self, schema, *args, **kwargs):
        super(DictField, self).__init__(*args, **kwargs)
        self._schema = schema

    @property
    def _type(self):
        return "Dict"

    def _get_fields(self):
        for key in dir(self._schema):
            if key.startswith("__"):
                continue
            subschema = getattr(self._schema, key)
            if not isinstance(subschema, Field):
                continue
            yield key, subschema

    def _validate(self, value):
        if not isinstance(value, dict):
            yield ([], "Not a dict")
            return
        value = dict(value)
        for key, subschema in self._get_fields():
            if key not in value:
                if getattr(subschema, "required", True):
                    yield ([], "Key \"{}\" is missing".format(key))
                # For some mysterious reason coverage module just ignores
                # the next line even though it is executed
                continue  # pragma: no cover
            subvalue = value.pop(key)
            for (child_path, error) in subschema.validate(subvalue):
                yield ([key] + child_path, error)
        if value:
            yield ([],
                   "Unkown fields: {}".format(", ".join(list(value.keys()))))

    def describe(self):
        for result in super(DictField, self).describe():
            yield result
        for key, subschema in self._get_fields():
            for (child_path, description) in subschema.describe():
                yield ([key] + child_path, description)

    def serialize(self, payload_object):
        ret_val = {}
        for key, subschema in self._get_fields():
            val = getattr(payload_object, key, None)
            ret_val[key] = None if val is None else subschema.serialize(val)
        return ret_val

    def deserialize(self, payload_dict):
        ret_val = self._schema()
        for key, subschema in self._get_fields():
            val = payload_dict.get(key, None)
            setattr(ret_val, key,
                    None if val is None else subschema.deserialize(val))
        return ret_val
