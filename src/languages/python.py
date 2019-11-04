from prtty import pretty
from populate import indent_to, populate_string
from lark import Transformer, Token, Tree, v_args
from funcy import merge, lmap, omit, concat
from ..parser import parser
from ..support import structure, types, composed_types

ELLIPSIS = "..."


@v_args(tree=True)
class AddInitializersMetas(Transformer):
    def get_initializer(self, node: Tree):
        initializer = {
            types.STR: lambda: "str($value)",
            types.INT: lambda: "int($value)",
            types.FLOAT: lambda: "float($value)",
            types.BOOL: lambda: "bool($value)",
            types.ANY: lambda: "$value",
            structure.REFERENCE: lambda: f"{node.children[0]}.from_($value)",
            composed_types.OBJECT: lambda: f"unexpected object",
            composed_types.UNION: lambda: "$value",
            composed_types.LIST: lambda: f'[{self.get_initializer(node.children[0]).replace("$value", "x")} for x in $value]',
        }[str(node.data)]()
        return initializer

    def required_pair(self, t):
        k, v = t.children
        initializer = self.get_initializer(v)
        if not isinstance(t._meta, dict):
            t._meta = {}
        t._meta = {**t._meta, "initializer": initializer}
        return t

    optional_pair = required_pair


imports = """
from typing import (Optional, List, Any)
from typing_extensions import Literal

"""


class Python(Transformer):
    def __init__(self, ref=None):
        self.ref = ref

    def __default__(self, data, children, meta):
        raise NotImplementedError(f"{data} is not implemented in grahql") from None

    def start(self, children):
        return imports + "\n".join(children)

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
        return "None"

    def literal_true(self, _):
        return f"Literal[True]"

    def literal_false(self, _):
        return f"Literal[False]"

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
        types = "\n".join([x for x, _, _ in children]) + "\n"
        arguments = ",\n".join([x for _, x, _ in children])
        initializers = ",\n".join([x for _, _, x in children])
        template = indent_to(
            "",
            """
            class $key(dictlike):
                ${{indent_to('    ', types)}}
                def __init__(
                    self,
                    *, 
                    ${{indent_to('        ', arguments)}}, 
                    **kwargs
                ):
                    super().__init__(
                        ${{indent_to('            ', initializers)}},
                        **kwargs
                    )
            """,
        )
        return populate_string(
            template,
            dict(
                types=types,
                arguments=arguments,
                initializers=initializers,
                indent_to=indent_to,
            ),
        )

    def list(self, children):
        value, = children
        return f"List[{value}]"

    def union(self, children):
        return f'Union[{", ".join(children)}]'

    @v_args(meta=True)
    def required_pair(self, children, meta):
        k, v = children
        if "$key" in v:
            return v.replace("$key", k)
        return k + ": " + v, k, f'{k}={meta["initializer"].replace("$value", k)}'

    @v_args(meta=True)
    def optional_pair(self, children, meta):
        k, v = children
        if "$key" in v:
            return v.replace("$key", k)
        else:
            return (
                f"{k}: Optional[{v}] = None\n",
                f"{k}=None",
                f'{k}={meta["initializer"].replace("$value", k)}',
            )

    def root_pair(self, children):
        k, v = children
        if "$key" in v:
            return v.replace("$key", k)
        else:
            return f"{k} = {v}\n{k}.from_ = lambda x: x\n"

    pass


def get_first_key(obj):
    keys = list(obj.keys())
    return keys[0]
