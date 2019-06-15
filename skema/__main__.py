# printf "\nA:\n  b: Str\n" | xargs -0I%  python -m src %

from .tokenize import tokenize
from .make_schema import make_schema
from .make_tree import make_tree
import sys
import json
from functools import reduce, partial
import jsonref
import fastjsonschema

rcompose = lambda *arr: reduce(lambda f, g: lambda *a, **kw: f(g(*a, **kw)), reversed(arr))


def to_jsonschema(schema, ref=None, resolve=False):
    
    result = rcompose(
        tokenize,
        make_tree,
        make_schema,
    )(schema)
    if ref and not ref in result.get('definitions', {}):
        raise Exception(f'can\'t find definition {ref}')

    reference = result['$ref'] if not ref else '#/definitions/' + ref
    resolver = fastjsonschema.RefResolver.from_schema(result,)
    if resolve:
        with resolver.resolving(reference) as result:
            return result
    else:
        result['$ref'] = reference
        return result

def main(schema, ref=None, resolve=False):
    return json.dumps(to_jsonschema(schema, ref, resolve), indent=4)

if __name__ == '__main__':
    string = sys.stdin.read()
    print(main(string))



