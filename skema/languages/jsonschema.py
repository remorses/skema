from prtty import pretty
from lark import Token
from ..transformers import Transformer
from funcy import merge, lmap, omit
from ..parser import parser

ELLIPSIS = "..."


class JsonSchema(Transformer):
    def __init__(self, ref=None):
        self.ref = ref

    def start(self, children):
        ref = self.ref or get_first_key(children[0])
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$ref": "#/definitions/" + ref,
            "definitions": merge(*children),
        }

    def type_str(self, _):
        return {"type": "string"}

    def type_bool(self, _):
        return {"type": "boolean"}

    def type_int(self, _):
        return {"type": "number", "multipleOf": 1.0}

    def type_float(self, _):
        return {"type": "number"}

    def type_any(self, _):
        return {}

    def literal_null(self, _):
        return {"const": None}

    def literal_true(self, _):
        return {"const": True}

    def literal_false(self, _):
        return {"const": False}

    def literal_string(self, children):
        value, = children
        return {"const": value[1:-1]}

    def literal_integer(self, children):
        value, = children
        return {"const": int(value)}

    def literal_ellipsis(self, _):
        return ELLIPSIS

    def regex(self, children):
        value, = children
        return {"type": "string", "pattern": value[1:-1]}

    def reference(self, children):
        value, = children
        return {"$ref": f"#/definitions/{value}"}

    def annotation(self, children):
        value, = children
        return value

    # TODO remove and make range better
    def scalar(self, children):
        value, = children
        return value

    def bounded_range(self, children):
        are_floats = any(["." in x for x in children])
        if are_floats:
            children = lmap(float, children)
        else:
            children = lmap(int, children)
        low, high = children
        res = {"type": "number", "minimum": low, "maximum": high}
        if not are_floats:
            res.update({"multipleOf": 1.0})
        return res

    def low_bounded_range(self, children):
        are_floats = any(["." in x for x in children])
        if are_floats:
            children = lmap(float, children)
        else:
            children = lmap(int, children)
        low, = children
        res = {"type": "number", "minimum": low}
        if not are_floats:
            res.update({"multipleOf": 1.0})
        return res

    def high_bounded_range(self, children):
        are_floats = any(["." in x for x in children])
        if are_floats:
            children = lmap(float, children)
        else:
            children = lmap(int, children)
        high, = children
        res = {"type": "number", "maximum": high}
        if not are_floats:
            res.update({"multipleOf": 1.0})
        return res

    def object(self, children):
        required = [
            get_first_key(c) for c in children if c != ELLIPSIS and c["required"]
        ]
        children = lmap(lambda o: omit(o, ["required"]), children)
        properties = merge(*children)
        if ELLIPSIS in children:
            children.remove(ELLIPSIS)
            if len(children) == 1:
                res = {"type": "object"}
            else:
                res = {"type": "object", "properties": properties}
        else:
            res = {
                "type": "object",
                "properties": properties,
                "additionalProperties": False,
                "required": required,
            }
        if required:
            res.update({"required": required})
        return res

    def list(self, children):
        value, = children
        return {"type": "array", "items": value}

    def union(self, children):
        if all(["const" in x for x in children]):
            return {"enum": children}
        return {"anyOf": children}

    def intersection(self, children):
        return {"allOf": children}

    def required_pair(self, children):
        if len(children) == 3:
            annotation, key, value = children
        else:
            key, value = children
            annotation = ""
        res = {str(key): {**value, "description": str(annotation)}, "required": True,}
        return res

    def root_pair(self, children):
        if len(children) == 3:
            annotation, key, value = children
        else:
            key, value = children
            annotation = ""
        res = {str(key): {"title": str(key), "description": str(annotation), **value}}
        return res

    def optional_pair(self, children):
        key, value = children
        res = {str(key): value, "required": False}
        return res

    pass


def get_first_key(obj):
    keys = list(obj.keys())
    return keys[0]
