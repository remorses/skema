import json
from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
import pytest
from graphql import build_schema
from graphql import build_schema
from .data import strings
from .support import keys, values
from skema.to_graphql import extract_references, to_graphql, merge_ands, replace_types, merge_scalar_unions, remove_ellipses


@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_extract_references(string):
    tokens = tokenize(string)
    tree = make_tree(tokens)
    print()
    print(tree.parent_relation())
    refs = extract_references(tree, [])
    print('len', len(refs))
    res = '\n\n'.join([(r.parent_relation()) for r in refs])
    print(res)
    print()
    res = '\n\n'.join([str(r) for r in refs])
    print(res)
    print()

@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_to_graphql(string):
    tokens = tokenize(string)
    tree = make_tree(tokens, )
    print()
    print(tree)
    refs = extract_references(tree, [])
    refs = [merge_ands(r, refs) for r in refs]
    refs = [remove_ellipses(r,) for r in refs]
    refs = merge_scalar_unions(refs)
    refs = [replace_types(r,) for r in refs]
    refs = [to_graphql(r, ) for r in refs]
    res = '\n\n'.join(refs)
    print(res)
    # build_schema(res)
    print()