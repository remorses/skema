try:
    from graphql import build_schema, DocumentNode
    from graphql.language.ast import (
        Node,
        ObjectTypeDefinitionNode,
        UnionTypeDefinitionNode,
        ScalarTypeDefinitionNode,
        FragmentDefinitionNode,
        EnumTypeDefinitionNode,
        FieldDefinitionNode,
    )
except ImportError:
    raise Exception('need graphql-core package to reconstruct graphql')
from .print_graphql_schema import print_schema
from skema.parser import parse
from lark import Tree

def reconstruct(string) -> Tree:
    schema = build_schema(string)
    skema = print_schema(schema)
    print(skema.replace(' ', '.'))
    return parse(skema)
