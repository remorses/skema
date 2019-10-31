from lark import Visitor, Tree
from copy import copy

def make_reference(id, tree: Tree):
    old_children = copy(tree.children)
    tree.children = [Tree("reference", [id])]
    subs = Tree("root_pair", [id] + old_children)
    return subs


class Splitter(Visitor):
    types: list

    def start(self, tree: Tree):
        tree.children.extend(self.types)

    def __init__(self):
        self.types = []
        pass

    def list(self, tree: Tree):
        child, = tree.children
        id = "_"
        if child.data in ["object", "list"]:
            self.types.append(make_reference(id, tree))
        pass

    def object(self, tree: Tree):
        for key in tree.children:
            name, value = key.children # TODO sometimes first is annotation
            if value.data in ['object']:
                print('ok')
                id = '_'
                self.types.append(Tree("root_pair", [id] + copy(key.children[1:])))
                key.children = [name, Tree("reference", [id])]

