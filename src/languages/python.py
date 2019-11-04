from prtty import pretty
from populate import indent_to, populate_string
from lark import Transformer, Token, Tree
from funcy import merge, lmap, omit, concat
from ..parser import parser

ELLIPSIS = "..."


class Python(Transformer):
    def __init__(self, ref=None):
        self.ref = ref

    def __default__(self, data, children, meta):
        raise NotImplementedError(f"{data} is not implemented in grahql") from None

    def start(self, children):
        return "\n".join(children)

    def type_str(self, _):
        return "str"

    def type_bool(self, _):
        return "bool"

    def type_int(self, _):
        return "int"

    def type_float(self, _):
        return "float"

    def type_any(self, _):
        return "Any"

    def literal_null(self, _):
        return 'None'

    def literal_true(self, _):
        return f'Literal[True]'

    def literal_false(self, _):
        return f'Literal[False]'

    def literal_string(self, children):
        value, = children
        return f"Literal[{value}]"

    def literal_number(self, children):
        value, = children
        return f"Literal[{value}]"

    def literal_ellipsis(self, _):
        return ELLIPSIS

    def regex(self, children):
        # value, = children
        return "str"

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

        template = """
        class ${{typename}}(dotdict):
            _schema: dict

            ${{indent_to('    ', render_hints(hints, args)) + '\\n'}}

            def __init__(
                self, 
                *, 
                ${{indent_to('        ', render_args(args, hints)) }}, 
                **kwargs
            ):
                super().__init__(
                    ${{indent_to('            ', render_setters(setters, args))}},
                    **kwargs
                )
        """
        types = "\n".join(children)
        template = indent_to(
            "",
            """
            class $key(dictlike):
                ${{indent_to('    ', types)}}
            """,
        )
        return populate_string(template, dict(types=types, indent_to=indent_to))

    def list(self, children):
        value, = children
        return f"List[{value}]"

    def union(self, children):
        return f'Union[{", ".join(children)}]'

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
            return f"{k} = {v}\n"

    pass


def get_first_key(obj):
    keys = list(obj.keys())
    return keys[0]
