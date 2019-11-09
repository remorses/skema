import fire
import json
import sys
from skema.resolve_refs import resolve_refs
import skema.generators as gens
from skema.parser import parse


def as_list(x):
    if isinstance(x, (list, tuple)):
        return x
    return [x]


def write(path, data):
    with open(path) as f:
        f.write(data)


def get_stdin() -> str:
    if sys.stdin.isatty():
        print("need skema from stdin")
        return
    lines = list(sys.stdin)
    lines = [l for l in lines if l.strip()]
    string = "".join(lines) + "\n"
    return string


class Gen:

    def python(self,):
        stdin = get_stdin()
        tree = parse(stdin)
        code = gens.python(tree)
        print(code.strip())

    def typescript(self,):
        stdin = get_stdin()
        tree = parse(stdin)
        code = gens.typescript(tree)
        print(code.strip())

    def jsonschema(self, ref=None, resolve=False):
        stdin = get_stdin()
        tree = parse(stdin)
        obj = gens.jsonschema(tree, ref=ref, resolve=resolve)
        code = json.dumps(obj, indent=4)
        print(code.strip())

    def graphql(self,):
        stdin = get_stdin()
        tree = parse(stdin)
        code = gens.graphql(tree)
        print(code.strip())

class FakeData:
    pass

class InferJson:
    pass

class FromCode:
    pass

Cli = {
    'gen': Gen,
    'fakedata': FakeData, # cat schema.skema | skema fakedata json > data.json
    # 'from': FromCode, # skema from jsonschema -f schema.json -t skema.skema
    # 'inferjson': InferJson # cat data.json | skema inferjson > skema.skema
}