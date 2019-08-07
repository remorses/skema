
from functools import reduce
from .constants import *
from .constants import constants
from .support import capitalize, is_and_key, is_or_key, is_object, is_and_object, is_leaf_key
import json


tab = '    '

def get_annotation(node):
    return node.annotation


class Node:
    def __init__(self, value, parent=None, required=True): 
        # optional when key is optional, so children[0] is optional
        # &, Node(&).children, every property of every child is grouped
        # |, one of children is valid
        self.value = value.strip() if isinstance(value, str) else value
        self.children = []
        self.parent = parent
        self.required = required
        self.annotation = ''
        self.pattern = ''
        self.implements = []
        self.is_interface = False
    
    def insert(self, *nodes):
        [self.children.append(n) for n in nodes]
        return self
    def append(self, nodes):
        for n in nodes:
            n = copy(n)
            n.parent = self
            self.children.append(n)
        return self
    def __repr__(self, ):
        return 'Node(value=' + (str(self.value) + (':' if len(self.children) else '')) + ')'
    
    def __str__(self, indent=''):
        res = (indent + str(self.value) or '""')
        annotation = get_annotation(self)
        res += ' (' + annotation + ')' if annotation else ''
        res += ':' if len(self.children) else ''
        for c in self.children:
            res += '\n' + Node.__str__(c, indent + tab)
        return res
    
    def parent_relation(self, indent=''):
        res = ''
        res += indent + (self.parent.value if self.parent else 'None') + ' -> '
        res += (str(self.value) or '""')
        res += ':' if len(self.children) else ''
        for c in self.children:
            res += '\n' + Node.parent_relation(c, indent + tab)
        return res

    def to_skema(self, indent='', res = ''):
        if self.value in [AND, OR, LIST]:
            res += ''
        elif not self.children and self.value != ELLIPSIS:
            res += str(self.value)
            res += ':' if len(self.children) else ''
        else:
            annotation = get_annotation(self)
            res += (indent + f'"""{annotation}"""\n' ) if annotation else ''
            res += (indent + str(self.value) or '""')
            res += ':' if len(self.children) else ''
            
        if is_and_object(self): # interface
            print(repr(self))
            for c in self.children[0].children:
                 res += ' ' + Node.to_skema(c, '') + ' &'
            for c in self.children[1:]:
                    res = Node.to_skema(c, indent + tab, res=res + '\n')

            # past_line = len(indent)
            # res = res[:-1]

            # using_interfaces_in_new_line = False
            # if using_interfaces_in_new_line:
            #     res += indent + Node.to_skema(c, '', ) + ' &'
            # else:

        elif is_key(self): # is_key(self): # key
            c = self.children[0]
            if self.value == LIST: # key: [Node]
                if is_end_key(self) and self.children[0].value != ELLIPSIS:
                    res += '[' + Node.to_skema(c, '', ) + ']'
                else:
                    # print(c.value)
                    # indent += tab if self.parent and self.parent.parent else '' # references that are list gets too indented
                    obj = '\n' + Node.to_skema(c, indent + tab,)
                    res += '[' + obj + '\n' + indent + ']'
            else: # key: Node
                if (len(c.children) == 0 and c.value != ELLIPSIS) or c.value in [AND, OR, LIST]: # dont go \n
                    res += ' ' + Node.to_skema(c, indent, )
                else:
                    res += '\n' + Node.to_skema(c, indent + tab, )
        else:
            if self.value in [OR, AND]: # Node | Node
                children = self.children[:]
                for i, c in enumerate(self.children):
                    if len(c.children):
                        pass
                        # raise Exception('can\'t handle object inside or, and')
                symbol = ' | ' if self.value == OR else ' & '
                for c in children[:-1]:
                    res += '' + Node.to_skema(c, '', ) + symbol
                res += '' + Node.to_skema(children[-1], '', )
            elif self.value == LIST: # [ object ]
                obj = ''
                # indent += tab if self.parent and self.parent.parent else '' # references that are list gets too indented
                for c in self.children:
                    obj += '\n' + Node.to_skema(c, indent + tab, )
                res += '[' + obj + '\n' + indent + ']' # TODO
            else: # object
                for c in self.children:
                    res = Node.to_skema(c, indent + tab, res=res + '\n')
        return res
    def to_graphql(self, indent='',):
        res = ''
        if is_leaf_key(self): # alias
            res += 'scalar '
            res += str(self.value)
        elif is_or_key(self) and all(['"' in c.value for c in self.children[0].children]):
            res += 'enum '
            res += str(self.value)
            res += ' {'
            for c in self.children[0].children:
                value = c.value.replace('"', '')
                res += '\n' + tab + value # TODO enum values should get namespace
            res += '\n}'
        elif is_or_key(self):
            res += 'union '
            res += str(self.value)
            res += ' = '
            for c in self.children:
                res += Node.to_skema(c, indent + tab, )
            # res += '\n'
        elif is_object(self):
            res += 'type ' if not self.is_interface else 'interface '
            res += str(self.value)
            res += (' implements ' + ' & '.join(self.implements)) if self.implements else ''
            res += ' {'
            for c in self.children:
                res += '\n' + Node.to_skema(c, indent + tab, )
            res += '\n}'
        else:
            err = f'no valid graphql\n{str(self)}'
            print(err)
            return ''
            raise NotImplementedError(err)
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

def is_key(node):
    return len(node.children) == 1

def is_end_key(node):
    if len(node.children) == 1:
        child = node.children[0]
        return (
            (is_end_type(child)) or
            (child.value in [LIST, OR, AND] and all([is_end_type(x) for x in child.children]))
        )
    else:
        return False

def is_end_type(node):
    return not node.children

def copy(node: Node):
    res = Node(node.value, node.parent)
    if len(node.children):
        res.insert(*[copy(c) for c in node.children])
    return res