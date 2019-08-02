
from functools import reduce
from .constants import *
import json

tab = '    '

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
            res += '\n' + Node.__str__(c, indent + tab)
        return res
    
    def str(self,):
        reference_bucket = []
        res = self.to_skema(bucket=reference_bucket)
        # print(reference_bucket)
        while len(reference_bucket):
            reference = reference_bucket.pop()
            res += '\n\n'
            res += reference.to_skema(bucket=reference_bucket)
        return res


    def to_skema(self, indent='', bucket=[]): # TODO remove bucket arg
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
                if 1: # not len(c.children):
                    res += '[' + Node.to_skema(c, '', bucket) + ']'
                else: # make reference for object (more than 1 children)
                    raise NotImplementedError(repr(c.children))
                    # res += '[\n' + Node.to_skema(c, indent + tab*2, bucket) + '\n' + indent + tab + ']' # TODO
            else: # key: Node
                if len(c.children) == 0 or c.value in [AND, OR, LIST]: # dont go \n
                    res += ' ' + Node.to_skema(c, '', bucket)
                else:
                    res += '\n' + Node.to_skema(c, indent + tab, bucket)
        else:
            if self.value in [OR, AND]: # Node | Node
                children = self.children[:]
                for i, c in enumerate(self.children):
                    if len(c.children):
                        raise Exception('can\'t handle object inside or, and')
                symbol = ' | ' if self.value == OR else ' & '
                for c in children[:-1]:
                    res += '' + Node.to_skema(c, '', bucket) + symbol
                res += '' + Node.to_skema(children[-1], '', bucket)
            elif self.value == LIST: # [ object ]
                obj = ''
                indent += tab if self.parent and self.parent.parent else '' # references that are list gets too indented
                for c in self.children:
                    obj += '\n' + Node.to_skema(c, indent + tab, bucket)
                res += '[' + obj + '\n' + indent + ']' # TODO
            else: # object
                for c in self.children:
                    res += '\n' + Node.to_skema(c, indent + tab, bucket)
        return res

def make_references(node: Node): # TODO assert name does nort already exist
    reference_name = node.value.capitalize()
    reference = Node(reference_name, node.parent)
    reference_body = Node(node.value, node.parent)
    for c in node.children:
        reference_body = reference_body.insert(c)
    reference = reference.insert(reference_body)
    return reference
    

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