from prtty import pretty
from skema.lark import Token, Tree, v_args
from ..lark import Transformer
from funcy import merge, lmap, omit, concat
from ..parser import parser
from ..support import modifiers
from .support import is_float

ELLIPSIS = "..."


class Graphql(Transformer):
    def __init__(self, ref=None):
        self.ref = ref

    def __default__(self, data, children, meta):
        raise NotImplementedError(f"{data} is not implemented in grahql") from None

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

    def bounded_range(self, children):
        l, h, = children
        if any([is_float(x) for x in [h, l]]):
            return 'Float'
        return 'Int'

    def low_bounded_range(self, children):
        value, = children
        if is_float(value):
            return 'Float'
        return 'Int'

    def high_bounded_range(self, children):
        value, = children
        if is_float(value):
            return 'Float'
        return 'Int'

    # def literal_null(self, _):
    #     raise NotImplementedError("null not exists in graphql")

    # def literal_true(self, _):
    #     raise NotImplementedError("true not exists in graphql")

    # def literal_false(self, _):
    #     raise NotImplementedError("false not exists in graphql")
    @v_args(tree=True)
    def literal_string(self, t):
        v, = t.children
        return v

    def literal_ellipsis(self, _):
        return ELLIPSIS

    def regex(self, children):
        # value, = children
        return "String"

    def reference(self, children):
        value, = children
        return str(value)

    def annotation(self, children):
        value, = children
        return str(value)

    def object(self, children):
        return "type $key {\n" + "\n".join(["    " + c for c in children]) + "\n}\n"

    def list(self, children):
        value, = children
        return f"[{value}]"

    def union(self, children):
        if all([isinstance(x, str) and '"' in x for x in children]):
            return (
                "enum $key {\n"
                + "\n".join(["    " + str(x[1:-1]) for x in children])
                + "\n}\n"
            )
        elif all([isinstance(x, str) for x in children]):
            return "union $key = " + " | ".join(children) + "\n"
        else:
            raise NotImplementedError("cannot mix literals and shit")

    def required_pair(self, children):
        k, v = children
        if "$key" in v:
            return v.replace("$key", k)
        if '"' in v:
            v = 'String'
        return k + ": " + v

    optional_pair = required_pair

    @v_args(meta=True)
    def root_pair(self, children, meta):
        k, v = children
        annotation = meta['annotation'] if 'annotation' in meta else ''    
        annotation = annotation and f'"""\n{annotation}\n"""\n'
        if modifiers.GRAPHQL_HIDDEN in annotation: # TODO graphql hide should be made before splitting
            return ''

        if modifiers.GRAPHQL_INPUT in annotation:
            v = v.replace('type ', 'input ')
            
        if "$key" in v:
            return annotation + v.replace("$key", k)
        else:
            return annotation + f"scalar {k}\n"

    pass


def get_first_key(obj):
    keys = list(obj.keys())
    return keys[0]
