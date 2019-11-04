from .parser import parse
from lark.visitors import TransformerChain
import src.languages as l
import src.transformers as t


def jsonschema(string):
    transformer = TransformerChain(l.JsonSchema())
    tree = parse(string)
    return transformer.transform(tree)


def python(string):
    transformer = TransformerChain(
        t.MergeIntersections(),
        t.GetDependencies(),
        t.AddListMetas(),
        t.AddUnionMetas(),
        t.Splitter(unions_inside_objects=False),
        l.Python(),
    )
    tree = parse(string)
    return transformer.transform(tree)

def typescript(string):
    transformer = TransformerChain(
        t.MergeIntersections(),
        t.GetDependencies(),
        t.AddListMetas(),
        t.AddUnionMetas(),
        t.Splitter(unions_inside_objects=False),
        l.Typescript(),
    )
    tree = parse(string)
    return transformer.transform(tree)


def graphq(string):
    transformer = TransformerChain(
        t.MergeIntersections(),
        t.GetDependencies(),
        t.AddListMetas(),
        t.AddUnionMetas(),
        t.Splitter(),
        t.Printer(),
        l.Graphql(),
    )
    tree = parse(string)
    return transformer.transform(tree)

