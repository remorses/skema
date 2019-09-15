from .tokenize import tokenize
from .make_schema import make_schema
from .make_tree import make_tree
from .resolve_refs import resolve_refs
from .support import rcompose


def to_jsonschema(schema, ref=None, resolve=False, hide=[], only=None):

    node = make_tree(tokenize(schema))
    result = make_schema(node)
    if ref and not ref in result.get("definitions", {}):
        raise Exception(f"can't find definition {ref}")

    if only and isinstance(only, list):
        result["definitions"] = {
            k: v for k, v in result["definitions"].items() if k in only
        }
    if hide and isinstance(hide, list):
        result["definitions"] = {
            k: v for k, v in result["definitions"].items() if not k in hide
        }

    result["$ref"] = result["$ref"] if not ref else "#/definitions/" + ref

    if resolve:
        resolve_refs(result)
        return result
    else:
        return result
