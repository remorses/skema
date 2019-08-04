from skema import tokenize, make_tree
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
                                    replace_aliases,
                                    replace_types
                                    )

def to_graphql(string):
    node = make_tree(tokenize(string))
    node = remove_ellipses(node)
    node = replace_aliases(node)
    print(node)
    refs = list(split_references(node))
    refs = [merge_ands(r, refs) for r in refs]
    refs = merge_scalar_unions(refs)
    refs = [replace_types(t) for t in refs]
    types = [t.to_graphql() for t in refs]
    schema = '\n\n'.join(types)
    return schema