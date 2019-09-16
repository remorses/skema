from typing import Union
from funcy import collecting
from populate import populate_string, indent_to
import json
import shutil
import requests
import fire
from skema.infer import from_jsonschema
from skema.to_jsonschema import to_jsonschema
from skema.generate import (
    generate_graphql,
    generate_types,
    generate_jsonschema,
    temporary_write,
    get_result_file,
)
from typing import *
from populate import populate_string, indent_to, render_dict


@collecting
def get_objects(schema):
    schema = to_jsonschema(schema)
    for name, body in schema.get("definitions", []).items():
        if (
            body.get("type", "") == "object"
            or body.get("type", "") == "array"
            or body.get("allOf")
            or body.get("anyOf")
            or body.get("oneOf")
        ):  
            if 'type' in body:
                type = body.get('type')
            elif '$ref' in body:
                type = body.get('$ref').split('/')[-1]

            yield name, type


imports = """
from typing import *
import skema
import fastjsonschema
"""


def generate_python_bilerplate(schema, hide=[], only=None):
    # get the main objects names from schema
    # generate a resolved jsonschema for each one
    names = get_objects(schema)
    if only:
        names = [x for x in names if x in only]
    if hide:
        names = [x for x in names if not x in hide]
    string = imports
    for typename in names:
        string += populate_string(
            template,
            dict(
                render_args=render_args,
                render_hints=render_hints,
                hints=dict(a="str", b="int"),
                args=dict(a=True, b=False),
                indent_to=indent_to,
                render_dict=render_dict,
                schema=to_jsonschema(schema, ref=typename, resolve=True),
                typename=typename,
            ),
        )
        string += '\n'
    return string


template = """
class ${{typename}}(dict):
    _schema = ${{ render_dict(schema) }}

    ${{indent_to('    ', render_hints(hints, args)) + '\\n'}}
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
    print(s)
    with open('example__.py', 'w') as f:
        f.write(s)

