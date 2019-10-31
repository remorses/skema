from lark import Visitor, Tree, Transformer
from funcy import cat, flip
from prtty import pretty
from collections import defaultdict
from .topological_sort import topological_sort
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

class MergeAnds(Transformer):
    types: dict = {}
    def __init__(self, ):
        pass

    def root_pair(self, children):
        key, *_ = children
        self.types[key] = Tree('root_pair', children)
        is_reference = lambda node: node.data == 'reference'
        for child in Tree('', children).find_pred(is_reference):
            print(child)
        # self.child_of
        return Tree('root_pair', children)

    # def intersection(self, tree: Tree):
    #     to_join = []
    #     for child in tree.children:
    #         if child.data == 'reference':
    #             ref, = child.children
    #             root_pair = self.types[ref]
    #             # only if object
    #             _, object = root_pair.children
    #             fields = object.children
    #             to_join += fields
    #         elif child.data == 'object':
    #             to_join += child.children
    #     tree.data = 'object'
    #     tree.children = to_join

    def intersection(self, children):
        to_join = []
        for child in children:
            if child.data == 'reference':
                ref, = child.children
                root_pair = self.types[ref]
                # only if object
                _, object = root_pair.children
                fields = object.children
                to_join += fields
            elif child.data == 'object':
                to_join += child.children
        return Tree('object', to_join)


is_reference_parent = lambda node: ( # TODO add list reference k case
    node.data in ['optional_pair', 'required_pair'] and node.children[1].data == 'reference'
)


class ReplaceIds(Transformer):
    types: dict = {}
    child_of: defaultdict = defaultdict(set)

    def __init__(self, ):
        pass

    def start(self, children):
        translations = {}
        ids_items = [(k, {x for x in v if x in self.child_of.keys()}) for k, v in self.child_of.items()]
        ids_sorted = topological_sort(ids_items)
        ids_sorted = (list(ids_sorted))
        for id in ids_sorted:
            translations[id] = '_'.join(reversed(list(self.child_of[id])))
            self.types[id].children[0] = translations[id]

            for _, parents in self.child_of.items():
                if id in parents:
                    parents.remove(id)
                    parents.add(translations[id])

            for parent in self.child_of[id]:
                original_id = flip(translations).get(parent)
                if not original_id in self.types:
                    continue
                refs = self.types[original_id].find_pred(lambda node: node.data == 'reference')
                for ref_node in refs:
                    refname, = ref_node.children
                    if refname in translations:
                        ref_node.children = [translations[refname]]
        return Tree('start', list(self.types.values()))
        

    def root_pair(self, children):
        key, *_ = children
        self.types[key] = Tree('root_pair', children)
        refs_parents = Tree('', children).find_pred(is_reference_parent)
        for child in refs_parents:
            parentname, ref = child.children # TODO first child might be annotation
            refname, = ref.children
            self.child_of[refname].add(str(key))
            self.child_of[refname].add(str(parentname))
        if refs_parents:
            pretty(self.child_of)
            pretty(list(self.types.keys()))
        return Tree('root_pair', children)



class Splitter(Transformer):
    types: dict = {}

    def root_pair(self, children):
        key, *_ = children
        self.types[key] = Tree('root_pair', children)
        return Tree('root_pair', children)

    def start(self, tree: Tree):
        types = list(self.types.values())
        # tree.children.extend(types)
        return Tree('start', types)

    def __init__(self, ):
        self.types = {}
        pass

    def list(self, children):
        child, = children
        id = make_id()
        if child.data in ["object", "list"]:
            old_children = copy(child.children)
            self.types[id] = Tree("root_pair", [id] + [Tree('object', old_children)])
        return Tree('list', [Tree("reference", [id])])

    def intersection(self, tree: Tree):
        raise Exception('cannot handle intersections')

    def object(self, children):
        for key in children:
            name, value = key.children # TODO sometimes first is annotation
            if value.data in ['object']:
                print('ok')
                id = make_id()
                self.types[id] = Tree("root_pair", [id] + copy(key.children[1:]))
                key.children = [name, Tree("reference", [id])]
        return Tree('object', children)






class SplitterVisitor(Visitor):
    types: dict = {}


    def root_pair(self, tree):
        key, *_ = tree.children
        self.types[key] = tree

    def start(self, tree: Tree):
        types = list(self.types.values())
        # tree.children.extend(types)
        tree.children = self.types.values()

    def __init__(self, ):
        self.types = {}
        pass

    def list(self, tree: Tree):
        child, = tree.children
        id = make_id()
        if child.data in ["object", "list"]:
            self.types[id] = make_reference(id, tree)
        pass

    def intersection(self, tree: Tree):
        raise Exception('cannot handle intersections')

    def object(self, tree: Tree):
        for key in tree.children:
            name, value = key.children # TODO sometimes first is annotation
            if value.data in ['object']:
                print('ok')
                id = make_id()
                self.types[id] = Tree("root_pair", [id] + copy(key.children[1:]))
                key.children = [name, Tree("reference", [id])]
