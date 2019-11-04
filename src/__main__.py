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


def gen(python=None, graphql=None, jsonschema=None):
    if python:
        if sys.stdin.isatty():
            print("need skema from stdin")
            return
        string = "".join(list(sys.stdin)).strip() + '\n'
        # print(string.replace(' ', '.'))
        code = gens.python(string)
        print(code.strip())


fire.Fire({"gen": gen})

