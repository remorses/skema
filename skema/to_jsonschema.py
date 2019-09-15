from .tokenize import tokenize
from .make_schema import make_schema
from .make_tree import make_tree
from .resolve_refs import resolve_refs
from .support import rcompose


def to_jsonschema(schema, ref=None, resolve=False, hide=[], only=None):

    node = make_tree(tokenize(schema))
    # if only and isinstance(only, list):
    #     node.children = [c for c in node.children if c.value in only]
    # if hide and isinstance(hide, list):
    #     node.children = [c for c in node.children if not c.value in hide]
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

    reference = result["$ref"] if not ref else "#/definitions/" + ref
    if reference not in result["definitions"].keys():
        reference = list(result["definitions"].keys())[0]
    result["$ref"] = reference

    if resolve:
        resolve_refs(result)
        return result
    else:
        return result
