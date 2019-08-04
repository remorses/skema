# printf "\nA:\n  b: Str\n" | xargs -0I%  python -m src %
import sys
import json
from functools import reduce, partial
from .to_jsonschema import to_jsonschema


def main(schema, ref=None, resolve=False):
    return json.dumps(to_jsonschema(schema, ref, resolve), indent=4)

if __name__ == '__main__':
    string = sys.stdin.read()
    print(main(string))



