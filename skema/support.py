import json
from functools import reduce
from .constants import *

log = lambda *x: None # print
# log = print

pretty = lambda x: print(json.dumps(x, indent=4, default=repr))

rcompose = lambda *arr: reduce(lambda f, g: lambda *a, **kw: f(g(*a, **kw)), reversed(arr))


def capitalize(s: str):
    if not s:
        return ''
    return s[0].capitalize() + s[1:]




def is_scalar(value):
    value = value.lower()
    scalars = [STR, STRING, INT, FLOAT, REGEX, ANY, NULL, BOOL]
    if value in [x.lower() for x in scalars]:
        return True
    if '"' in value:
        return True
    if '..' in value:
        return True
    if '//' in value:
        return True
    return False


def is_key(node):
    """opoosto di leaf o di oggetto"""
    return len(node.children) == 1

def is_and_key(node):
    return is_key(node) and node.children[0].value in [AND,]

def is_and_object(node):
    return is_object(node) and node.children[0].value in [AND,]

def is_or_key(node):
    return is_key(node) and node.children[0].value in [OR,]

def is_list_key(node):
    return is_key(node) and node.children[0].value in [LIST,]


def is_enum_key(node):
    return is_or_key(node) and all(['"' in c.value for c in node.children[0].children])


def is_object(node):
    return (
        len(node.children) >= 1
        and all([len(c.children) for c in node.children if c.value != ELLIPSIS])
        and node.value not in [AND, OR, LIST,]
        # node.children[0] not in [c for c in constants if c != ELLIPSIS]
    )



def is_leaf(node):
    return (
        not node.children
    )

def is_leaf_key(node):
    return (
        len(node.children) == 1
        and is_leaf(node.children[0])
    )