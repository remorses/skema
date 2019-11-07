try:
    from graphql import parse, DocumentNode
    from graphql.language.ast import (
        Node,
    
        ObjectTypeDefinitionNode,
        UnionTypeDefinitionNode,
        ScalarTypeDefinitionNode,
        FragmentDefinitionNode,
        EnumTypeDefinitionNode,
        FieldDefinitionNode,
    )
except ImportError:
    raise Exception('need graphql-core package to reconstruct graphql')
from lark import Tree
from typing import List
from ..support import literals, structure, composed_types, types


def is_terminal(node):
    TERMINALS = []
    if isinstance(node, TERMINALS):
        return True
    return False


class Reconstructor:
    def terminal_type(self, name):
        switch = {
            'String': types.STR,
            'Boolean': types.BOOL,
            'Json': types.ANY,
            'Int': types.INT,
            'Floar': types.FLOAT,
            'ID': types.STR,
        }
        return switch.get(name, name)

    def object(self, node: ObjectTypeDefinitionNode):    
        def get_pair(child: FieldDefinitionNode):
            if is_terminal(child):
                return Tree(structure.REQUIRED_PAIR, child.name.value, self.terminal_type(child.type.name.value))
            elif is_list(child):
                return Tree(composed_types.LIST, )

        children = [get_pair(x) for x in node.fields]
        return Tree(composed_types.OBJECT, children)

    def start(self, doc: DocumentNode):
        def get_root_pairs(doc: DocumentNode) -> Tree:
            for node in doc.definitions:
                if isinstance(node, ObjectTypeDefinitionNode):
                    tree = self.object(node)
                    yield Tree(structure.ROOT_PAIR, tree)
        defs = list(get_root_pairs(doc))
        return Tree(structure.START, defs)

def reconstruct(string):
    doc = parse(string)
