# printf "\nA:\n  b: Str\n" | xargs -0I%  python -m src %
import sys
import json
from functools import reduce, partial
import fastjsonschema


from .tokenize import tokenize
from .make_schema import make_schema
from .make_tree import make_tree
from .resolve_refs import resolve_refs

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
    result['$ref'] = reference
    if resolve:
        resolve_refs(result)
        return result
    else:
        return result

def main(schema, ref=None, resolve=False):
    return json.dumps(to_jsonschema(schema, ref, resolve), indent=4)

if __name__ == '__main__':
    string = sys.stdin.read()
    print(main(string))



