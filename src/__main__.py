import fire
import sys
import src.generators as gens


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
    string = "".join(list(sys.stdin)).strip() + "\n"
    return string


def gen(python=None, graphql=None, typescript=None, jsonschema=None):
    stdin = get_stdin()
    if python:
        code = gens.python(stdin)
    elif typescript:
        code = gens.typescript(stdin)
    elif graphql:
        code = gens.graphql(stdin)
    elif jsonschema:
        code = gens.jsonschema(stdin)
    else:
        code = ""
    print(code.strip())


fire.Fire({"gen": gen})

