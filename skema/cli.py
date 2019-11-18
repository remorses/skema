import fire
import json
import sys
from skema.resolve_refs import resolve_refs
import skema.generators as gens
from skema.parser import parse
from skema.reconstruct import from_graphql, from_jsonschema


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
    def python(self, skema=""):
        """
        """
        if not skema:
            skema = get_stdin()
        tree = parse(skema)
        code = gens.python(tree)
        print(code.strip())
        return code.strip()

    def typescript(self, skema=""):
        """
        """
        if not skema:
            skema = get_stdin()
        tree = parse(skema)
        code = gens.typescript(tree)
        print(code.strip())
        return code.strip()

    def jsonschema(self, ref=None, resolve=False, skema=""):
        """
        Root:
            ref: Str
            resolve: Bool
        """
        if not skema:
            skema = get_stdin()
        tree = parse(skema)
        obj = gens.jsonschema(tree, ref=ref, resolve=resolve)
        code = json.dumps(obj, indent=4)
        print(code.strip())
        return code.strip()

    def graphql(self, skema=""):
        """
        """
        if not skema:
            skema = get_stdin()
        tree = parse(skema)
        code = gens.graphql(tree)
        print(code.strip())
        return code.strip()


class FakeData:
    pass


class InferJson:
    pass


class FromCode:
    def jsonschema(self, ref=None):
        stdin = get_stdin()
        obj = json.loads(stdin)
        tree = from_jsonschema(obj, ref=ref)
        code = gens.skema(tree)
        print(code.strip())

    def graphql(self,):
        stdin = get_stdin()
        code = from_graphql(stdin)
        print(code.strip())


def print_tree():
    stdin = get_stdin()
    t = parse(stdin)
    print(t.pretty())


Cli = {
    "to": Gen,
    "from": FromCode,
    "fakedata": FakeData,  # cat schema.skema | skema fakedata json > data.json
    "tree": print_tree
    # 'from': FromCode, # skema from jsonschema -f schema.json -t skema.skema
    # 'inferjson': InferJson # cat data.json | skema inferjson > skema.skema
}
