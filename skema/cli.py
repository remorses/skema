import fire
import json
import sys
from skema.resolve_refs import resolve_refs
import skema.generators as gens


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


class Cli:
    def python(self,):
        stdin = get_stdin()
        code = gens.python(stdin)
        print(code.strip())

    def typescript(self,):
        stdin = get_stdin()
        code = gens.typescript(stdin)
        print(code.strip())

    def jsonschema(self, ref=None, resolve=False):
        stdin = get_stdin()
        obj = gens.jsonschema(stdin, ref=ref, resolve=resolve)
        code = json.dumps(obj, indent=4)
        print(code.strip())

    def graphql(self,):
        stdin = get_stdin()
        code = gens.graphql(stdin)
        print(code.strip())

