from lark import Visitor, Tree
import uuid
from copy import copy

def make_reference(id, tree: Tree):
    old_children = copy(tree.children)
    tree.children = [Tree("reference", [id])]
    subs = Tree("root_pair", [id] + old_children)
    return subs

def make_id():
    id = str(uuid.uuid1())[:8]
    return id

class MakeMap(Visitor):
    types: dict

    def __init__(self):
        self.types = {}
        pass

    def root_pair(self, tree):
        key, *_ = tree.children
        self.types[key] = tree

class Splitter(Visitor):
    types: list

    def start(self, tree: Tree):
        types = list(self.types.values())
        tree.children.extend(types)

    def __init__(self, types={}):
        self.types = types
        pass

    def list(self, tree: Tree):
        child, = tree.children
        id = make_id()
        if child.data in ["object", "list"]:
            self.types[id] = make_reference(id, tree)
        pass

    def intersection(self, tree: Tree):
        to_join = []
        for child in tree.children:
            if child.data == 'reference':
                ref, = child.children
                root_pair = self.types[ref]
                # only if object
                _, object = root_pair.children
                fields = object.children
                to_join += fields
            elif child.data == 'object':
                to_join += child.children
        tree.data = 'object'
        tree.children = to_join

    def object(self, tree: Tree):
        for key in tree.children:
            name, value = key.children # TODO sometimes first is annotation
            if value.data in ['object']:
                print('ok')
                id = make_id()
                self.types[id] = Tree("root_pair", [id] + copy(key.children[1:]))
                key.children = [name, Tree("reference", [id])]

