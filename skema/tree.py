
from functools import reduce
from .constants import *
import json



class Node:
    def __init__(self, value, parent=None, required=True): 
        # TODO 
        # optional when key is optional, so children[0] is optional
        # &, Node(&).children, every property of every child is grouped
        # |, one of children is valid
        self.value = value.strip() if isinstance(value, str) else value
        self.children = []
        self.parent = parent
        self.required = required
        self.child_annotations = []
        self.pattern = ''
    
    def insert(self, *nodes):
        [self.children.append(n) for n in nodes]
        return self
    
    def __repr__(self, ):
        return str(self.value) + ':' if len(self.children) else ''
    
    def __str__(self, indent=''):
        res = (indent + str(self.value) or '""')
        annotations = self.parent.child_annotations if self.parent else []
        res += ' (' + annotations.pop(0) + ')' if len(annotations) else ''
        res += ':' if len(self.children) else ''
        for c in self.children:
            res += '\n' + Node.__str__(c, indent + '\t')
        return res
    
    def to_skema(self, indent=''):
        if self.value not in [LIST, OR, AND]:
            res = (indent + str(self.value) or '""')
            annotations = self.parent.child_annotations if self.parent else []
            res += ' (' + annotations.pop(0) + ')' if len(annotations) else ''
            res += ':' if len(self.children) else ''
        else:
            res = indent + ''
        
        if len(self.children) == 1: # key
            c = self.children[0]
            if self.value == LIST: # key: [Node]
                if not len(c.children):
                    res += '[' + Node.to_skema(c, '') + ']'
                else: # make reference for object (more than 1 children)
                    raise NotImplementedError(repr(c.children))
                    res += '[\n' + Node.to_skema(c, indent + '\t\t') + '\n' + indent + '\t' + ']' # TODO
            else: # key: Node
                if len(c.children) == 0 or c.value in [AND, OR, LIST]: # dont go \n
                    res += '' + Node.to_skema(c, ' ')
                else:
                    res += '\n' + Node.to_skema(c, indent + '\t')
        else:
            if self.value in [OR, AND]: # Node | Node
                # TODO make indenpendant skemas for children that are not objects
                # replace these nodes with Node(reference_name, c.parent)
                symbol = ' | ' if self.value == OR else ' & '
                for c in self.children[:-1]:
                    res += '' + Node.to_skema(c, '') + symbol
                res += '' + Node.to_skema(self.children[-1], '')
            elif self.value == LIST: # [ object ]
                obj = ''
                indent += '\t'
                for c in self.children:
                    obj += '\n' + Node.to_skema(c, indent + '\t')
                res += '[' + obj + '\n' + indent + ']' # TODO
            else: # object
                for c in self.children:
                    res += '\n' + Node.to_skema(c, indent + '\t')
        return res



def tree_from_dict(obj: dict, key='root'):
    node = Node(key)
    for k, val in obj.items(): # properties
        if isinstance(val, dict): # is_object
            node.insert(tree_from_dict(val, k))
        else:
            node.insert(Node(k,).insert(Node(val,)))
    return node


def map_tree(f, node, result=Node('')):
    if not node.children:
        f(node)
    else:
        for child in node.children:
            f(child)
    return result

def traverse_tree(f, node, result=[]):
    if not node.children:
        result.append(f(node))
    else:
        for child in node.children:
            traverse_tree(f, child, result)
    return result