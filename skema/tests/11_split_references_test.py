import json
import random

import pytest
from graphql import build_schema
from skema.split_references import (FORBIDDEN_TYPE_NAMES,
                                    breadth_first_traversal, get_leaves,
                                    is_valid_as_reference,
                                    search_cascaded_name,
                                    remove_objects_inside_lists
                                    )
from skema.tree import Node

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
    print(nodes)
    for i in range(1, len(nodes)):
        name = nodes[i].value
        computed = search_cascaded_name(node, name)
        print(computed)
        assert all([x not in computed for x in FORBIDDEN_TYPE_NAMES])

@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_is_valid_as_reference(string):
    node = make_tree(tokenize(string))
    print(node)
    def op(node: Node):
        return is_valid_as_reference(node), repr(node)
    nodes = list(breadth_first_traversal(node, op))
    print('\n'.join(map(repr, nodes)))
