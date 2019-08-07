from skema import tokenize, make_tree
from funcy import rcompose, partial, tap
import operator
from skema.tree import copy, Node
from typing import List, Callable, Tuple
from skema.support import is_leaf_key, is_scalar
from skema.split_references import (FORBIDDEN_TYPE_NAMES,
                                    breadth_first_traversal, get_leaves,
                                    is_valid_as_reference,
                                    search_cascaded_name,
                                    remove_ellipses,
                                    remove_nulls,
                                    # dereference_objects_inside_lists,
                                    split_references,
                                    merge_ands,
                                    merge_scalar_unions,
                                    # replace_aliases,
                                    replace_types,
                                    get_alias_nodes,
                                    INTERFACE_END_KEYWORD,
                                    mark_enums,
                                    )



def remove_ands(refs): 
    refs_and_indexes = [merge_ands(r, refs) for r in refs]
    refs = [ref for ref, indexes in refs_and_indexes]
    # use them as implements
    indexes = set([i for ref, indexes in refs_and_indexes for i in indexes])
    indexes = sorted(indexes, reverse=True)
    interfaces = [copy(refs[i]) for i in indexes]
    for node in interfaces:
        node.value = node.value + INTERFACE_END_KEYWORD
        node.is_interface = True
    leaves = [leaf for r in refs for leaf in get_leaves(r) if r.value.lower() != 'root'] # TODO presume no root
    for i in indexes:
        if not [l for l in leaves if l.value == refs[i].value]:
            refs.pop(i)
    return refs + interfaces

def search_non_existing_subgroup(subgroup: Tuple[str, ...], groups: List[Tuple[str, ...]]) -> Tuple[str, ...]:
    subgroup = ('', ) + subgroup
    while len(subgroup) > 1:
        if subgroup[1:] not in groups:
            subgroup = subgroup[1:]
        else:
            # print('FOUND', subgroup)
            break
    return subgroup

def search_existing_subgroup(subgroup: Tuple[str, ...], groups: List[Tuple[str, ...]]) -> Tuple[str, ...]:
    subgroup = ('', ) + subgroup
    while len(subgroup) > 1:
        if subgroup not in groups:
            subgroup = subgroup[1:]
        else:
            # print('FOUND', subgroup)
            break
    # print('subgroup', subgroup)
    return subgroup

def remove_parent_names(refs: List[Node]) -> List[Node]:
    refs = sorted(refs, key=lambda v: len(v.value))
    ref_names = [n.value if isinstance(n.value, tuple) else (n.value,) for n in refs]
    assert len(set(ref_names)) == len(ref_names)
    for ref in refs:
        ref.value = ref.value if isinstance(ref.value, tuple) else (ref.value,)
        other_ref_names = [r.value for r in refs if r.value != ref.value]
        subgroup = search_non_existing_subgroup(ref.value, other_ref_names)
        ref.value = subgroup
        # print('ref.value', ref.value)
    # print([r.value for r in refs])
    return [compute_new_names(ref, [r.value for r in refs]) for ref in refs]

def compute_new_names(node: Node, ref_names: List[str]) -> Node:
    leaves = get_leaves(node)
    leaves_to_compute = [l for l in leaves if isinstance(l.value, tuple)]
    # print('leaves_to_compute', leaves_to_compute)
    for leaf in leaves_to_compute:
        subgroup = search_existing_subgroup(leaf.value, ref_names)
        leaf.value = subgroup
    return node
        
def remove_tuples(refs: List[Node]) -> List[Node]:
    for ref in refs:
        nodes = breadth_first_traversal(ref)
        for node in nodes:
            if isinstance(node.value, tuple):
                node.value = ''.join(node.value)
    return refs



preprocess_refs = rcompose(
    remove_parent_names,
    # mark_enums,
    remove_tuples,
    remove_ands,
    merge_scalar_unions,
    lambda refs: [replace_types(r, refs) for r in refs],
    partial(filter, lambda x: x.value.lower() != 'root'),
    list,
)

json_alias = Node('Json').append([Node('')])

scalar_already_present = [ # empty to make tests pass
    # 'Json', 
    # 'DateTime',
    # 'Time',
    # 'Date',
]

def to_graphql(string: str, scalar_already_present=scalar_already_present) -> str:
    node = make_tree(tokenize(string))
    node = remove_ellipses(node)
    node = remove_nulls(node)
    # node = replace_aliases(node)
    print(node)
    refs = [*get_alias_nodes(node)] + [*split_references(node)] + [json_alias]
    refs = preprocess_refs(refs)
    refs = [r for r in refs if not (is_leaf_key(r) and r.value in scalar_already_present)]
    types = [t.to_graphql() for t in refs]
    schema = '\n\n'.join(types)
    return schema