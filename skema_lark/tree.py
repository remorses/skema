from prtty import pretty
from lark import Transformer, Token
from funcy import merge, lmap, omit
from .parse import parser

ELLIPSIS = "..."


class TreeToJson(Transformer):
    def start(self, children):
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            #  "$ref": "#/definitions/" + children[0],
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
        if any(["." in x for x in children]):
            children = lmap(float, children)
        else:
            children = lmap(int, children)
        low, high = children
        return {"type": "number", "minimum": low, "maximum": high}

    def low_bounded_range(self, children):
        if any(["." in x for x in children]):
            children = lmap(float, children)
        else:
            children = lmap(int, children)
        low, = children
        return {"type": "number", "minimum": low}

    def high_bounded_range(self, children):
        if any(["." in x for x in children]):
            children = lmap(float, children)
        else:
            children = lmap(int, children)
        high, = children
        return {"type": "number", "maximum": high}

    def object(self, children):
        required = [
            get_first_key(c) for c in children if c != ELLIPSIS and c["required"]
        ]
        children = lmap(lambda o: omit(o, ["required"]), children)
        properties = merge(*children)
        if ELLIPSIS in children:
            children.remove(ELLIPSIS)
            if len(children) == 1:
                return {"type": "object", "required": required}

            return {"type": "object", "properties": properties, "required": required}
        else:
            return {
                "type": "object",
                "properties": properties,
                "additionalProperties": False,
                "required": required,
            }

    def list(self, children):
        value, = children
        return {"type": "array", "items": value}

    def union(self, children):
        return {"anyOf": children}

    def intersection(self, children):
        return {"allOf": children}

    def required_pair(self, children):
        if len(children) == 3:
            annotation, key, value = children
        else:
            key, value = children
            annotation = ""
        res = {str(key): value, "required": True, "description": str(annotation)}
        return res

    def optional_pair(self, children):
        key, value = children
        res = {str(key): value, "required": False}
        return res

    pass


def get_first_key(obj):
    keys = list(obj.keys())
    return keys[0]


def parse(x):
    tree = parser.parse(x)
    print(tree.pretty())
    return TreeToJson().transform(tree)


x = '''
obj: Str
"""
ciao
"""
x:
    y: Str
    z: "Str"
    v: 4
    b: X
    oo:
        a: [Str]
    ll: [
        x: Int
        u: Str
    ]
    x: /xxx/

z: 0 .. 1
x: 0 | 1 | 4
xxx: Name | Str & Int
'''
pretty(parse(x))
