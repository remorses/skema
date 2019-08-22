from .tree import Node
from .support import is_key, is_leaf_key

def get_alias_nodes(node: Node):
    for c in node.children: # TODO this presume tree has Root
        if is_leaf_key(c):
            yield c

def remove_hidden_fields(node, language):
    indicator = f'[hide {language}]'
    aliases = get_alias_nodes(node)
    to_remove = [x.value for x in aliases if indicator in x.annotation]
    return recursize_remove_hidden_fields(node, indicator, to_remove)

def recursize_remove_hidden_fields(node: Node, indicator, aliases_to_remove):
    if not node.children:
        return
    for c in node.children:
        has_alias_to_remove = lambda x: (is_key(x) and x.children[0].value in aliases_to_remove)
        node.children = [x for x in node.children if not indicator in x.annotation and not has_alias_to_remove(x)]
        recursize_remove_hidden_fields(c, indicator, aliases_to_remove)
    return node