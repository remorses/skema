from .parser import parse
from lark.visitors import TransformerChain
import skema.languages as l
import skema.transformers as t
from .resolve_refs import resolve_refs

def jsonschema(string, ref=None, resolve=False):
    transformer = TransformerChain(l.JsonSchema(ref=ref))
    tree = parse(string)
    data = transformer.transform(tree)
    if resolve:
        resolve_refs(data)
    return data


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
