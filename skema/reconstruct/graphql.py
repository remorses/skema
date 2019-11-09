from skema.parser import parse
from skema.lark import Tree

def reconstruct(string) -> str:
    try:
        from graphql import build_schema, DocumentNode
        from .print_graphql_schema import print_schema
    except ImportError:
        raise Exception('need graphql-core package to reconstruct graphql')
    schema = build_schema(string)
    skema = print_schema(schema)
    # print(skema.replace(' ', '.'))
    return skema
    # return parse(skema)
