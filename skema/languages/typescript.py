from prtty import pretty
from populate import indent_to, populate_string
from skema.lark import Token, Tree, v_args
from funcy import merge, lmap, omit, concat
from ..lark import Transformer
from ..parser import parser

ELLIPSIS = "..."


class Typescript(Transformer):
    def __init__(self, ref=None):
        self.ref = ref

    def __default__(self, data, children, meta):
        raise NotImplementedError(f"{data} is not implemented in grahql") from None

    def start(self, children):
        return "\n".join(children)

    def type_str(self, _):
        return "string"

    def type_bool(self, _):
        return "boolean"

    def type_int(self, _):
        return "number"

    def type_float(self, _):
        return "number"

    def type_any(self, _):
        return "any"

    def literal_null(self, _):
        return "null"

    def literal_true(self, _):
        return f"true"

    def literal_false(self, _):
        return f"false"

    def bounded_range(self, children):
        l, h, = children
        return 'number'

    def low_bounded_range(self, children):
        value, = children
        return 'number'

    def high_bounded_range(self, children):
        value, = children
        return 'number'

    def literal_string(self, children):
        value, = children
        return f'{value}'

    def literal_number(self, children):
        value, = children
        return str(value)

    def literal_ellipsis(self, _):
        return ELLIPSIS

    def regex(self, children):
        # value, = children
        return "string"

    def reference(self, children):
        value, = children
        return value

    def annotation(self, children):
        value, = children
        return value


    def object(self, children):
        types = "\n    ".join(children)  # .replace(' ', '.')
        return "export interface $key {\n    " + types + "\n}\n"

    def list(self, children):
        value, = children
        return f"Array<{value}>"

    def union(self, children):
        return " | ".join(children)

    def required_pair(self, children):
        k, v = children
        if "$key" in v:
            return v.replace("$key", k)
        return k + ": " + v

    def optional_pair(self, children):
        k, v = children
        if "$key" in v:
            return v.replace("$key", k)
        return k + "?: " + v

    @v_args(meta=True)
    def root_pair(self, children, meta):
        k, v = children
        annotation = meta['annotation'] if 'annotation' in meta else ''    
        annotation = annotation and f'/*\n{annotation}\n*/\n'
        if "$key" in v:
            return annotation + v.replace("$key", k)
        else:
            return annotation + f"export type {k} = {v}\n"

    pass


def get_first_key(obj):
    keys = list(obj.keys())
    return keys[0]
