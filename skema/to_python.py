import copy
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
from .split_references import is_big_list, replace_occurrences, stronger_type, get_leaves
from functools import reduce
from .support import (capitalize, is_and_key, is_enum_key, is_key, is_list_key, topological_sort,
                      is_object, is_or_key, is_scalar, is_leaf, is_leaf_key, is_and_object)



imports = """
from typing import Any, Optional, List, Union, Callable
from typing_extensions import Literal
import skema
import fastjsonschema
from prtty import prettify
lmap = lambda func: lambda xs: list(map(func, xs))

class dotdict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__
"""

def is_circular(schema):
    try:
        json.dumps(schema)
    except Exception:
        return True

def get_local_schema(schema, typename,):
    try:
        schema = to_jsonschema(schema, ref=typename, resolve=True)
        if is_circular(schema):
            return to_jsonschema(schema, ref=typename, resolve=False)
        else:
            return schema
    except Exception as e:
        print(e)
        return {}

map_simple_types = dict( # TODO i am mapping from graphql types
    String='str',
    Str='str',
    str='str',
    Int='int',
    Float='float',
    null='None',
    Bool='bool',
    Boolean='bool',
    Any='Any',
    Json='Any',
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
        return "'" + key + "'"

def get_initializer(node: Node):
    key = node.children[0].value
    if key in map_simple_types:
        return None
    else:
        if key == OR:
            if any(['"' in c.value for c in node.children[0].children]):
                return None
            return f'dotdict'
        elif key == LIST:
            return f'lmap({get_initializer(node.children[0])})'
        elif key == ANY:
            return None
        return f'{key}.from_dict'


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
    options = ["'" + c.value + "'" if not '"' in c.value else c.value for c in node.children]
    options = [f'Literal[{n}]' if '"' in n else n for n in options]
    return f'Union[{", ".join(options)}]'



# def get_dependencies(node: Node):
#     global scalars
#     leaves = get_leaves(node)
#     scalars = [s.lower() for s in scalars]
#     def is_reference(x: Node):
#         return x.value.lower() not in scalars and not '"' in x.value
#     return set(x for x in leaves if is_reference(x) and x.value != node.value)


# def move_dependencies_up(refs):
#     refs = [(r, get_dependencies(r)) for r in refs]
#     print(refs)
#     return topological_sort(refs)
#     # return [x for x, _ in refs]


def merge_scalars(references):
    scalars = [STR, STRING, INT, FLOAT, REGEX, ANY, NULL, BOOL, 'Json']
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
    # refs = move_dependencies_up(refs)
    # refs = [x for x in refs if not is_leaf_key(x)]
    print('\n\n'.join([str(x) for x in refs]))
    string = imports
    string += populate_string(exports, dict(
        all=[n.value for n in refs],
    ))
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
        setters = {c.value: get_initializer(c) for c in node.children}
        # print(local_schema)
        string += populate_string(
            template,
            dict(
                hints=hints,
                args=args,
                setters=setters,
                typename=typename,
                render_args=render_args,
                render_setters=render_setters,
                render_hints=render_hints,
                indent_to=indent_to,
                render_dict=render_dict,
            ),
        )
        string += '\n'
    for node in refs:
        typename = node.value
        local_schema = get_local_schema(schema, typename)
        string += populate_string(
            bottom,
            dict(
                schema=local_schema,
                typename=typename,
                render_dict=render_dict,
            ),
        )
    return string

exports = '''
__all__ = (
    ${{ indent_to('    ', '\\n'.join(['"' + x + '",' for x in all])) }}
)
'''

bottom = '''
${{typename}}._schema = ${{ render_dict(schema) }}
${{typename}}.validate_ = staticmethod(fastjsonschema.compile(${{typename}}._schema))

'''
template = """
class ${{typename}}(dict):
    _schema: dict
    validate_: staticmethod

    ${{indent_to('    ', render_hints(hints, args)) + '\\n'}}
    def __getattr__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            return object.__getattribute__(self, name)
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
    @classmethod
    def from_dict(cls, obj: dict):
        assert isinstance(obj, dict)
        return cls(**obj)
    def validate(self):
        return self.validate_(self)
    @classmethod
    def fake(cls, resolvers={}):
        return cls(**(skema.fake_data(${{typename}}._schema, amount=1, from_json=True, resolvers=resolvers)[0] or {}))
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    def __repr__(self):
        return f'${{typename}}({prettify(self)})'


"""


def render_hints(hints: Dict[str, str], args: Dict[str, str]):
    hints = [
        f"{name}: Optional[{type}]" if args[name] else f"{name}: {type}"
        for name, type in hints.items()
    ]
    return "\n".join(hints)


def render_args(fields: Dict[str, bool], hints: Dict[str, str], default=lambda k: "None"):
    required_fields = [x for x, is_optional in fields.items() if not is_optional]
    optional_fields = [x for x, is_optional in fields.items() if is_optional]
    required_args = [f"{name}: {hints[name]}" for name in required_fields]
    optional_args = [f"{name}: {hints[name]}={default(name)}" for name in optional_fields]
    return ",\n".join(required_args + optional_args)


def render_setters(setters: Dict[str, str], args: Dict[str, bool]):
    args = [f"{name}={(initializer + '(' + name + ')' + f' if {name} != None else {name}') if initializer else name}" for name, initializer in setters.items()]
    return ",\n".join(args)


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

