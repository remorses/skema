from typing import Union
from funcy import collecting
from populate import populate_string, indent_to
import json
import shutil
import requests
import fire
from skema.infer import from_jsonschema
from .tree import Node, is_leaf_key
from skema.to_jsonschema import to_jsonschema
from typing import *
from populate import populate_string, indent_to, render_dict
from .constants import *
from .split_tree_parts import split_tree_parts
from .split_references import is_big_list, replace_occurrences, stronger_type
from functools import reduce
from .support import (capitalize, is_and_key, is_enum_key, is_key, is_list_key,
                      is_object, is_or_key, is_scalar, is_leaf, is_leaf_key, is_and_object)



imports = """
from typing import *
from typing_extensions import Literal
import skema
import fastjsonschema
"""
def get_local_schema(schema, typename):
    try:
        return to_jsonschema(schema, ref=typename, resolve=True),
    except Exception as e:
        print(e)
        return {}

map_simple_types = dict(
    String='str',
    Str='str',
    Int='int',
    Float='float',
    null='None',
    Bool='bool',
    Any='Any',
)
def map_type(node: Node):
    if node.value in [OR]:
        raise Exception('non so che fare')
    key = node.children[0].value
    if key in map_simple_types:
        return map_simple_types[key]
    else:
        if key == OR:
            return handle_union(node.children[0])
        elif key == LIST:
            return f'List[{map_type(node.children[0])}]'
        return key


def is_valid_as_reference(key: Node): # for graphql
    def is_valid_key(key):
        if is_or_key(key):
            return True
        if not is_key(key):
            return False
        list_node = key.children[0]
        return not is_big_list(list_node)
    # true se è un oggetto con solo leaf_key oppure con piccole liste come figli
    if is_object(key) and not is_list_key(key) and all([is_leaf_key(c) or is_valid_key(c) for c in key.children]):
        return True
    if is_and_key(key) or is_and_object(key):
        return True
    if is_big_list(key):
        return True
    return False


def handle_union(node: Node):
    options = [c.value for c in node.children]
    options = [f'Literal[{n}]' if '"' in n else n for n in options]
    return f'Union[{", ".join(options)}]'



scalars = [STR, STRING, INT, FLOAT, REGEX, ANY, NULL, BOOL]
def merge_scalars(references):
    to_delete = {}
    for node in references:
        is_scalar_leafe = (is_key(node) and node.children[0].value in scalars)
        if is_scalar_leafe:
            new_type = map_type(node)
            obj = {node.value: new_type}
            # print('new_type', obj)
            to_delete.update(obj)
    # print('to_delete', to_delete)
    for ref in references:
        replace_occurrences(ref, to_delete)
    return [r for r in references if not r.value in to_delete.keys()]


def to_python(schema, hide=[], only=None):
    # get the main objects names from schema
    # generate a resolved jsonschema for each one
    refs = split_tree_parts(schema, 'python', is_valid_as_reference=is_valid_as_reference,  hide=hide, only=only)
    refs = list(reversed(refs))
    refs = merge_scalars(refs)
    # refs = [x for x in refs if not is_leaf_key(x)]
    print('\n\n'.join([str(x) for x in refs]))
    string = imports
    for node in refs:
        typename = node.value
        if is_leaf_key(node):
            string += f'{typename} = {map_type(node)}' + '\n'
            continue
        if node.children[0].value == OR:
            string += f'{typename} = ' + handle_union(node.children[0]) + '\n'
            continue
        args = {c.value: not c.required for c in node.children}
        hints = {c.value: map_type(c) for c in node.children}
        string += populate_string(
            template,
            dict(
                hints=hints,
                args=args,
                # schema=get_local_schema(schema, typename),
                schema = {},
                typename=typename,
                render_args=render_args,
                render_hints=render_hints,
                indent_to=indent_to,
                render_dict=render_dict,
            ),
        )
        string += '\n'
    return string


template = """
class ${{typename}}(dict):
    _schema = ${{ render_dict(schema) }}

    ${{indent_to('    ', render_hints(hints, args)) + '\\n'}}
"""
"""
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    def __getattr__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            return object.__getattribute__(self, name)
    def __init__(self, *, ${{render_args(args)}}):
        super().__init__(${{render_args({k: True for k in args}, default=lambda k: k)}})
    def validate(self):
        return self.validate_(self)
    @staticmethod
    def fake(resolvers={}):
        return skema.fake_data(${{typename}}._schema, amount=1, from_json=True, resolvers=resolvers)[0]
${{typename}}.validate_ = fastjsonschema.compile(${{typename}}._schema)
"""


def render_hints(hints: Dict[str, str], args: Dict[str, str]):
    hints = [
        f"{name}: Optional[{type}]" if args[name] else f"{name}: {type}"
        for name, type in hints.items()
    ]
    return "\n".join(hints)


def render_args(fields: Dict[str, bool], default=lambda k: "None"):
    required_fields = [x for x, is_optional in fields.items() if not is_optional]
    optional_fields = [x for x, is_optional in fields.items() if is_optional]
    required_args = [f"{name}" for name in required_fields]
    optional_args = [f"{name}={default(name)}" for name in optional_fields]
    return ", ".join(required_args + optional_args)


if __name__ == "__main__":
    s = imports
    s += populate_string(
        template,
        dict(
            render_args=render_args,
            render_hints=render_hints,
            typename="Classe",
            hints=dict(a="str", b="int"),
            args=dict(a=True, b=False),
            indent_to=indent_to,
            schema={},
            render_dict=render_dict,
        ),
    )
    # print(s)
    with open('example__.py', 'w') as f:
        f.write(s)

