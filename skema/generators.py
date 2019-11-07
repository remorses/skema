from .parser import parse
from lark.visitors import TransformerChain
import skema.languages as l
import skema.transformers as t
from .resolve_refs import resolve_refs


def jsonschema(tree, ref=None, resolve=False):
    transformer = TransformerChain(l.JsonSchema(ref=ref))
    data = transformer.transform(tree)
    if resolve:
        resolve_refs(data)
    return data


def python(tree):
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

    return transformer.transform(tree)


def typescript(tree):
    transformer = TransformerChain(
        t.RemoveAnnotations(),
        t.MergeIntersections(),
        t.GetDependencies(),
        t.AddListMetas(),
        t.AddUnionMetas(),
        t.Splitter(unions_inside_objects=False),
        l.Typescript(),
    )
    return transformer.transform(tree)


def graphql(tree):
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

    return transformer.transform(tree)
