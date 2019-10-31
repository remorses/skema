from prtty import pretty
from .splitter import Splitter
from lark import Transformer, Token, Tree
from funcy import merge, lmap, omit, concat
from .parse import parser

ELLIPSIS = "..."


class Enumeration:
    children: list


class Object:
    fields: list


class List:
    fields: list


class Graphql(Transformer):
    def __init__(self, ref=None):
        self.ref = ref

    def start(self, children):
        return "\n".join(children)

    def type_str(self, _):
        return "String"

    def type_bool(self, _):
        return "Boolean"

    def type_int(self, _):
        return "Int"

    def type_float(self, _):
        return "Float"

    def type_any(self, _):
        return "Json"

    def literal_null(self, _):
        raise NotImplementedError("null not exists in graphql")

    def literal_true(self, _):
        raise NotImplementedError("true not exists in graphql")

    def literal_false(self, _):
        raise NotImplementedError("false not exists in graphql")

    # def literal_string(self, children):
    #     value, = children
    #     return value

    def literal_integer(self, children):
        raise NotImplementedError("literal integers not exists in graphql")

    def literal_ellipsis(self, _):
        return ELLIPSIS

    def regex(self, children):
        # value, = children
        return "String"

    def reference(self, children):
        value, = children
        return value

    def annotation(self, children):
        value, = children
        return value

    # TODO remove and make range better
    def scalar(self, children):
        value, = children
        return value

    def object(self, children):
        return "type $key {\n" + "\n".join(["    " + c for c in children]) + "\n}\n"

    def list(self, children):
        value, = children
        return f"[{value}]"

    def union(self, children):
        if all([isinstance(x, Tree) and x.data == "literal_string" for x in children]):
            return (
                "enum $key {\n"
                + "\n".join(["    " + str(x.children[0][1:-1]) for x in children])
                + "\n}\n"
            )
        elif all([isinstance(x, str) for x in children]): 
            return "type $key = " + " | ".join(children) + "\n"
        else:
            raise NotImplementedError('cannot mix literals and shit')

    def required_pair(self, children):
        k, v = children
        if "$key" in v:
            return v.replace("$key", k)
        return k + ": " + v
    
    def root_pair(self, children):
        k, v = children
        if "$key" in v:
            return v.replace("$key", k)
        else:
            return f'scalar {k}\n'

    pass


def get_first_key(obj):
    keys = list(obj.keys())
    return keys[0]


def parse(x):
    tree = parser.parse(x)
    print(tree.pretty())
    return Graphql().transform(tree)


x = """
obj:
    a: Str
    b: Int
    z:
        a: Int
        b: Str
        x: [
            x: Int
            y: Float
        ]

xxx: String | Int
zzz: String &
    x: Int

"""

t = parser.parse(x)
print(t.pretty())
t = Splitter().visit(t)
print(t.pretty())
s = Graphql().transform(t)
print(s)
