# from lark import Visitor, Tree, Transformer, Token, v_args
# from functools import partial
# from funcy import cat, flip, collecting
# from prtty import pretty
# from collections import defaultdict
# from toposort import toposort, toposort_flatten
# from ordered_set import OrderedSet
# from .types import UniqueKey
# import uuid
# from copy import copy


# # def make_reference(id, tree: Tree):
# #     old_children = copy(tree.children)
# #     tree.children = [Tree("reference", [id])]
# #     subs = Tree("root_pair", [id] + old_children)
# #     return subs


# # class MakeMap(Visitor):
# #     types: dict

# #     def __init__(self):
# #         self.types = {}
# #         pass

# #     def root_pair(self, tree):
# #         key, *_ = tree.children
# #         self.types[key] = tree


# # i could remove this class by
# # getting the path from root to leaf for the node i am removing,
# # make the name of the reference as the join of the parent names
# class ReplaceIds(Transformer):
#     types: dict = {}
#     child_of: defaultdict = defaultdict(set)

#     def __init__(self,):
#         pass

#     def start(self, children):
#         translations = {}
#         ids_items = [
#             (k, {x for x in v if x in self.child_of.keys()})
#             for k, v in self.child_of.items()
#         ]
#         ids_sorted = topological_sort(ids_items)
#         ids_sorted = list(ids_sorted)
#         for id in ids_sorted:
#             translations[id] = "_".join(reversed(list(self.child_of[id])))
#             self.types[id].children[0] = translations[id]

#             for _, parents in self.child_of.items():
#                 if id in parents:
#                     parents.remove(id)
#                     parents.add(translations[id])

#             for parent in self.child_of[id]:
#                 original_id = flip(translations).get(parent)
#                 if not original_id in self.types:
#                     continue
#                 refs = self.types[original_id].find_pred(
#                     lambda node: node.data == "reference"
#                 )
#                 for ref_node in refs:
#                     refname, = ref_node.children
#                     if refname in translations:
#                         ref_node.children = [translations[refname]]
#         return Tree("start", list(self.types.values()))

#     def root_pair(self, children):
#         key, *_ = children
#         self.types[key] = Tree("root_pair", children)

#         # get generic references
#         refs_parents = Tree("", children).find_pred(is_reference_parent)
#         for child in refs_parents:
#             parentname, ref = child.children 
#             refname, = ref.children
#             self.child_of[refname].add(str(key))
#             self.child_of[refname].add(str(parentname))

#         # get list references
#         list_refs_parents = list(Tree("", children).find_pred(is_reference_list_parent))
#         for list_parent in list_refs_parents:
#             parentname, list_node, = list_parent.children
#             ref, = list_node.children
#             refname, = ref.children
#             self.child_of[refname].add(str(key))
#             self.child_of[refname].add(str(parentname))

#         # if refs_parents:
#         #     pretty(self.child_of)
#         #     pretty(list(self.types.keys()))
#         return Tree("root_pair", children)


# # class SplitterVisitor(Visitor):
# #     types: dict = {}


# #     def root_pair(self, tree):
# #         key, *_ = tree.children
# #         self.types[key] = tree

# #     def start(self, tree: Tree):
# #         types = list(self.types.values())
# #         # tree.children.extend(types)
# #         tree.children = self.types.values()

# #     def __init__(self, ):
# #         self.types = {}
# #         pass

# #     def list(self, tree: Tree):
# #         child, = tree.children
# #         id = make_id()
# #         if child.data in ["object", "list"]:
# #             self.types[id] = make_reference(id, tree)
# #         pass

# #     def intersection(self, tree: Tree):
# #         raise Exception('cannot handle intersections')

# #     def object(self, tree: Tree):
# #         for key in tree.children:
# #             name, value = key.children
# #             if value.data in ['object']:
# #                 print('ok')
# #                 id = make_id()
# #                 self.types[id] = Tree("root_pair", [id] + copy(key.children[1:]))
# #                 key.children = [name, Tree("reference", [id])]
