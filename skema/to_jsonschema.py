
from .tokenize import tokenize
from .make_schema import make_schema
from .make_tree import make_tree
from .resolve_refs import resolve_refs
from .support import rcompose



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