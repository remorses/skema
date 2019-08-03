from graphql import build_schema
import json
import random

import pytest
from graphql import build_schema
from skema.split_references import (FORBIDDEN_TYPE_NAMES,
                                    breadth_first_traversal, get_leaves,
                                    is_valid_as_reference,
                                    search_cascaded_name,
                                    remove_ellipses,
                                    is_scalar,
                                    dereference_objects_inside_lists,
                                    split_references,
                                    merge_ands,
                                    merge_scalar_unions
                                    )
from skema.tree import Node
from ..to_graphql import to_graphql, replace_types
from ..make_schema import make_schema
from ..make_tree import make_tree
from ..tokenize import tokenize
from .data import strings
from .support import keys, values


@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_get_leaves(string):
    node = make_tree(tokenize(string))
    print(node)
    leaves = get_leaves(node)
    print(leaves)

@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_bfs(string):
    node = make_tree(tokenize(string))
    print(node)
    nodes = list(breadth_first_traversal(node, ))
    print('\n'.join(map(repr, nodes)))
    nodes = [n for n in nodes if not is_scalar(n.value) and not n.value in FORBIDDEN_TYPE_NAMES]
    names = []
    for i in range(1, len(nodes)):
        computed = search_cascaded_name(node, nodes[i])
        print(computed + ' -> ' + nodes[i].value)
        names.append(computed)
        assert all([x not in computed for x in FORBIDDEN_TYPE_NAMES])
    print(nodes)
    assert len(names) == len(set(names))

@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_is_valid_as_reference(string):
    node = make_tree(tokenize(string))
    remove_ellipses(node)
    print(node)
    def op(node: Node):
        return is_valid_as_reference(node), repr(node)
    nodes = list(breadth_first_traversal(node, op))
    print('\n'.join(map(repr, nodes)))

@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_dereference_objects_inside_lists(string):
    node = make_tree(tokenize(string))
    remove_ellipses(node)
    refs = list(dereference_objects_inside_lists(node))
    print('\n'.join(map(repr, refs)))
    print(node)
    print('refs')
    for r in refs:
        print(r)

@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_split_references(string):
    node = make_tree(tokenize(string))
    remove_ellipses(node)
    print(node)
    refs = []
    # refs += list(dereference_objects_inside_lists(node))
    refs += list(split_references(node))
    refs += list(dereference_objects_inside_lists(node))
    print('\n'.join(map(repr, refs)))
    print()
    print('refs')
    for r in refs:
        print(r)
        print()

@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_to_gql(string):
    node = make_tree(tokenize(string))
    remove_ellipses(node)
    print(node)
    refs = []
    refs += list(split_references(node))
    refs += list(dereference_objects_inside_lists(node))
    refs = [merge_ands(r, refs) for r in refs]
    refs = merge_scalar_unions(refs)
    refs = [replace_types(t) for t in refs]
    types = [to_graphql(t) for t in refs]
    schema = '\n\n'.join(types)
    print(schema)
    build_schema(schema)
    


def test_if_im_dumb():
    assert is_scalar('"ciao"')