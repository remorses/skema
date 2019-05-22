
from functools import reduce

import json



class Node:
    def __init__(self, value, parent=None): 
        # TODO 
        # optional when key is optional, so children[0] is optional
        # &, Node(&).children, every property of every child is grouped
        # |, one of children is valid
        self.value = value
        self.children = []
        self.parent = parent
    
    def insert(self, *nodes):
        [self.children.append(n) for n in nodes]
        return self
    
    def __repr__(self, indent=''):
        res = (indent + str(self.value))
        res += ':' if len(self.children) else ''
        for c in self.children:
            res += '\n' + Node.__repr__(c, indent + '\t')
        return res



def tree_from_dict(obj: dict, key='root'):
    node = Node(key)
    for k, val in obj.items(): # properties
        if isinstance(val, dict): # is_object
            node.insert(tree_from_dict(val, k))
        else:
            node.insert(Node(k,).insert(Node(val,)))
    return node


