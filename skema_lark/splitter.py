from lark import Visitor, Tree, Transformer, Token, v_args
from functools import partial
from funcy import cat, flip, collecting
from prtty import pretty
from collections import defaultdict
from .topological_sort import topological_sort
from toposort import toposort, toposort_flatten
from orderedset import OrderedSet
from .types import UniqueKey
import uuid
from copy import copy

def make_reference(id, tree: Tree):
    old_children = copy(tree.children)
    tree.children = [Tree("reference", [id])]
    subs = Tree("root_pair", [id] + old_children)
    return subs



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
        children = unique(to_join, key=lambda x: x.children[0])
        return Tree('object', children)

@collecting
def unique(l, *, key):
    passed = set()
    for e in l:
        d = key(e)
        if not d in passed:
            yield e
        passed.add(d)


is_reference_parent = lambda node: ( # TODO add list reference k case
    node.data in ['optional_pair', 'required_pair'] and node.children[1].data == 'reference'
)

# is_reference_list_parent = lambda node: ( # TODO add list reference k case
#     node.data in ['optional_pair', 'required_pair'] and node.children[1].data == 'list' 
#     and (node.children[1].children[0].data == 'list')
# )

def is_reference_list_parent(node: Tree):
    is_list_pair = node.data in ['optional_pair', 'required_pair'] and node.children[1].data == 'list'
    if not is_list_pair:
        return False
    list_node = node.children[1]
    return str(list_node.children[0].data) == 'reference'

# i could remove this class by 
# getting the path from root to leaf for the node i am removing,
# make the name of the reference as the join of the parent names
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

        # get generic references
        refs_parents = Tree('', children).find_pred(is_reference_parent)
        for child in refs_parents:
            parentname, ref = child.children # TODO first child might be annotation
            refname, = ref.children
            self.child_of[refname].add(str(key))
            self.child_of[refname].add(str(parentname))
        
        # get list references
        list_refs_parents = list(Tree('', children).find_pred(is_reference_list_parent))
        for list_parent in list_refs_parents:
            parentname, list_node, = list_parent.children
            ref, = list_node.children
            refname, = ref.children
            self.child_of[refname].add(str(key))
            self.child_of[refname].add(str(parentname))

        # if refs_parents:
        #     pretty(self.child_of)
        #     pretty(list(self.types.keys()))
        return Tree('root_pair', children)


@v_args(tree=True)
class AddListMetas(Transformer):
    def required_pair(self, tree: Tree):
        name, list_node = tree.children
        if not list_node.data == 'list':
            return tree
        list_node._meta = {'parent_key': name}
        return tree
    
    optional_pair = required_pair
    root_pair = required_pair
        


class Splitter(Transformer):
    types: dict = {}
    tree: Tree
    dependencies: dict

    def transform(self, t):
        self.tree = t
        if not t.meta or not 'dependencies' in t.meta:
            raise Exception('needs tree with dependencies')
        self.dependencies = t.meta['dependencies']
        for k, v in t.meta['dependencies'].items():
            print(f'{k} -> {list(v)}')
        return super().transform(t)
    
    def make_id(self, key):
        print(repr(key))
        print(self.dependencies[key])
        if not key:
            return str(uuid.uuid1())[:8]
        if not isinstance(key, UniqueKey):
            key = UniqueKey(key)
        id = '_'.join(list(self.dependencies[key])) + '_' + str(key)
        assert id
        return id

    def root_pair(self, children):
        key, *_ = children
        self.types[key] = Tree('root_pair', children)
        return Tree('root_pair', children)

    def start(self, children):
        types = list(self.types.values())
        # tree.children.extend(types)
        return Tree('start', types)

    def __init__(self, ):
        self.types = {}
        pass

    @v_args(meta=True)
    def list(self, children, meta):
        child, = children
        if not child.data in ["object", "list"]:
            return Tree('list', children)
        parent_key = meta['parent_key']
        id = self.make_id(parent_key)
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
                id = self.make_id(name)
                self.types[id] = Tree("root_pair", [id] + copy(key.children[1:]))
                key.children = [name, Tree("reference", [id])]
        return Tree('object', children)



@v_args(tree=True)
class GetDependencies(Transformer):
    dependencies: defaultdict = defaultdict(OrderedSet)

    def start(self, tree):
        ordered_deps = list(toposort_flatten(self.dependencies_as_sets))
        for k in ordered_deps:
            v = self.dependencies[k]
            to_process = [x for x in v if x in self.dependencies]
            for x in to_process:
                self.dependencies[(k)].update(self.dependencies[x])
        return Tree("start", tree.children, meta={'dependencies': self.dependencies})

    @property
    def dependencies_as_sets(self,):
        return {k: set(v) for k, v in self.dependencies.items()}

    def required_pair(self, t,):
        this, value = t.children
        if value.data == 'object':
            for child in value.children:
                k, _ = child.children
                self.dependencies[UniqueKey(k)].add(UniqueKey(this))
        return t

    optional_pair = required_pair
    root_pair = required_pair





# class SplitterVisitor(Visitor):
#     types: dict = {}


#     def root_pair(self, tree):
#         key, *_ = tree.children
#         self.types[key] = tree

#     def start(self, tree: Tree):
#         types = list(self.types.values())
#         # tree.children.extend(types)
#         tree.children = self.types.values()

#     def __init__(self, ):
#         self.types = {}
#         pass

#     def list(self, tree: Tree):
#         child, = tree.children
#         id = make_id()
#         if child.data in ["object", "list"]:
#             self.types[id] = make_reference(id, tree)
#         pass

#     def intersection(self, tree: Tree):
#         raise Exception('cannot handle intersections')

#     def object(self, tree: Tree):
#         for key in tree.children:
#             name, value = key.children # TODO sometimes first is annotation
#             if value.data in ['object']:
#                 print('ok')
#                 id = make_id()
#                 self.types[id] = Tree("root_pair", [id] + copy(key.children[1:]))
#                 key.children = [name, Tree("reference", [id])]
