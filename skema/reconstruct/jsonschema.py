from skema.parser import parse
from random import randint
from funcy import omit
from lark import Tree, Token
import skema.reconstruct.schema_types as jsontypes
from ..support import composed_types, types, literals, structure
from ..dictlike import dictlike


def is_block(obj):
    ks = ["anyOf", "allOf", "oneOf", "type", "const"]
    return any([k in obj for k in ks])


def reconstruct(obj, definition_key="definitions", root_name="Root") -> Tree:
    nodes = []
    obj = dictlike(**obj)
    if definition_key in obj:
        for name, block in obj[definition_key].items():
            block = dictlike(block)
            t = Tree(structure.ROOT_PAIR, [make_token(name), process_block(block)])
            nodes.append(t)
    if is_block(obj):
        if "$ref" in obj:
            root_name = get_ref_name(obj)
        obj = omit(obj, ["$ref"])
        obj = dictlike(obj)
        t = Tree(structure.ROOT_PAIR, [make_token(root_name), process_block(obj)])
        nodes.append(t)
    return Tree(structure.START, nodes)
    # print(skema.replace(' ', '.'))

    # return parse(skema)


def get_ref_name(block):
    return block["$ref"].split("/")[-1]


def process_block(block: jsontypes.Block,):
    blocktype = block.get("type", "")
    if False:
        pass
    elif "$ref" in block:
        name = get_ref_name(block)
        return Tree(structure.REFERENCE, [name])
    elif "anyOf" in block:
        return Tree(
            composed_types.UNION,
            [process_block(dictlike(item)) for item in block.anyOf],
        )

    elif blocktype == "array":
        return Tree(composed_types.LIST, [process_block(dictlike(block["items"]))])
    elif blocktype == "object":
        pairtype = structure.REQUIRED_PAIR
        properties = block.get("properties", {})
        return Tree(
            composed_types.OBJECT,
            [
                Tree(pairtype, [make_token(k), process_block(dictlike(v))])
                for k, v in properties.items()
            ],
        )
    elif blocktype == "string":
        return make_type_tree(types.STR)
    elif blocktype == "integer":
        return make_type_tree(types.INT)
    elif blocktype == "number":
        return make_type_tree(types.FLOAT)
    elif blocktype == "boolean":
        return make_type_tree(types.BOOL)
    else:
        return make_type_tree(types.ANY)


def make_token(data):
    return Token("UNKNOWN", data, line=randint(1, 999), column=randint(1, 999))


def make_type_tree(data):
    data = make_token(data)
    return Tree(data, [])


"""
type == integer -> 
type == number -> 
type == string -> 
type == array -> Tree(list, [process_block(obj.items)])
type == object -> Tree(object, [Tree(pair, k, [process_block(v)] for k, v in obj.properties.items()]) 
type == or -> [Tree(union, [process_block(item)]) for item in obj.anyOf]
"""
