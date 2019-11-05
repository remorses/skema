from .parser import parse
from lark.visitors import TransformerChain
import src.languages as l
import src.transformers as t


def jsonschema(string, ref=None):
    transformer = TransformerChain(l.JsonSchema(ref=ref))
    tree = parse(string)
    return transformer.transform(tree)


def python(string):
    transformer = TransformerChain(
        t.RemoveAnnotations(),
        t.MergeIntersections(),
        t.GetDependencies(),
        t.AddListMetas(),
        t.AddUnionMetas(),
        t.Splitter(unions_inside_objects=False),
        t.SortOptionalsLast(),
        l.AddInitializersMetas(),
        l.Python(),
    )
    tree = parse(string)
    return transformer.transform(tree)


def typescript(string):
    transformer = TransformerChain(
        t.RemoveAnnotations(),
        t.MergeIntersections(),
        t.GetDependencies(),
        t.AddListMetas(),
        t.AddUnionMetas(),
        t.Splitter(unions_inside_objects=False),
        l.Typescript(),
    )
    tree = parse(string)
    return transformer.transform(tree)


def graphql(string):
    transformer = TransformerChain(
        t.RemoveAnnotations(),
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
