from prtty import pretty
from skema.lark import Token, v_args
from funcy import merge, lmap, omit
from ..parser import parser
from ..transformers import GetDependencies
from ..lark import chain_with, TopDownTransformer, Transformer
from ..support import composed_types

ELLIPSIS = "..."

class AddIndentsInMetas(TopDownTransformer):
    indent: int = 0

    def object(self, tree):
        self.indent += 1
        tree._meta.update({'indent': self.indent})
        self.visit_children(tree)
        self.indent -= 1

    def list(self, tree):
        if tree.children[0].data == composed_types.OBJECT:
            tree._meta.update({'indent': self.indent})
            self.visit_children(tree)
            

@chain_with([AddIndentsInMetas()])
class Skema(Transformer):
    def __init__(self, ref=None, tab='    '):
        self.indent = 0
        self.ref = ref
        self.tab = tab

    @v_args(meta=True)
    def start(self, children, m):
        # pretty(m)
        return '\n\n'.join(children)

    def type_str(self, _):
        return 'Str'

    def type_bool(self, _):
        return 'Bool'

    def type_int(self, _):
        return 'Int'

    def type_float(self, _):
        return 'Float'

    def type_any(self, _):
        return 'Any'

    def literal_null(self, _):
        return 'null'

    def literal_true(self, _):
        return 'true'

    def literal_false(self, _):
        return 'false'

    def literal_string(self, children):
        value, = children
        return value

    def literal_integer(self, children):
        value, = children
        return str(value)

    @v_args(tree=True)
    def literal_ellipsis(self, t):
        return '...'

    def regex(self, children):
        value, = children
        return value

    def reference(self, children):
        value, = children
        return value

    # def annotation(self, children):
    #     value, = children
    #     return value

    def bounded_range(self, children):
        l, h, = children
        return f'{l} .. {h}'

    def low_bounded_range(self, children):
        x, = children
        return f'{x} ..'

    def high_bounded_range(self, children):
        x, = children
        return f'.. {x}'

    @v_args(meta=True)
    def object(self, children, m):
        sep = '\n' + m['indent'] * self.tab
        s = sep + sep.join(children)
        return s

    @v_args(meta=True)
    def list(self, children, m):
        value, = children
        if 'indent' in m:
            indent = m['indent'] * self.tab
            return f'[{indent}{value}\n{indent}]'
        return f'[{value}]'
        

    def union(self, children):
        return ' | '.join(children)

    def intersection(self, children):
        return ' & '.join(children)

    def required_pair(self, children):
        key, value = children
        return f'{key}: {value}'

    root_pair = required_pair

    def optional_pair(self, children):
        key, value = children
        return f'{key}?: {value}'

    pass


def get_first_key(obj):
    keys = list(obj.keys())
    return keys[0]
