from .parser import parser
from lark.visitors import TransformerChain
import src.languages as l
import src.transformers as t


def jsonschema(string):
    transformer = TransformerChain(
        l.JsonSchema(),
    )
    tree = parser.parse(string)
    return transformer.transform(tree)


def python(string):
    transformer = TransformerChain(
        t.MergeIntersections(),
        t.GetDependencies(),
        t.AddListMetas(),
        t.AddUnionMetas(),
        t.Splitter(),
        l.Python(),
    )
    tree = parser.parse(string)
    return transformer.transform(tree)


def graphq(string):
    transformer = TransformerChain(
        t.MergeIntersections(),
        t.GetDependencies(),
        t.AddListMetas(),
        t.AddUnionMetas(),
        t.Splitter(),
        l.Graphql(),
    )
    tree = parser.parse(string)
    return transformer.transform(tree)

