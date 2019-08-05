from skema import tokenize, make_tree
from skema.tree import copy, Node
from skema.split_references import (FORBIDDEN_TYPE_NAMES,
                                    breadth_first_traversal, get_leaves,
                                    is_valid_as_reference,
                                    search_cascaded_name,
                                    remove_ellipses,
                                    is_scalar,
                                    # dereference_objects_inside_lists,
                                    split_references,
                                    merge_ands,
                                    merge_scalar_unions,
                                    # replace_aliases,
                                    replace_types,
                                    get_alias_nodes,
                                    INTERFACE_END_KEYWORD
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


def to_graphql(string):
    node = make_tree(tokenize(string))
    node = remove_ellipses(node)
    # node = replace_aliases(node)
    print(node)
    refs = []
    refs += list(get_alias_nodes(node))
    refs += list(split_references(node))
    print(refs)
    refs = [r for r in refs if r.value.lower() != 'root'] # TODO presume root
    refs = remove_ands(refs)
    refs = merge_scalar_unions(refs)
    refs = [replace_types(t) for t in refs]
    types = [t.to_graphql() for t in refs]
    schema = '\n\n'.join(types)
    return schema