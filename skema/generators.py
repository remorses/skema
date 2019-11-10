from .parser import parse
from lark.visitors import TransformerChain
import skema.languages as l
import skema.transformers as t
from .resolve_refs import resolve_refs


def jsonschema(tree, ref=None, resolve=False):
    transformer = TransformerChain(
        t.RemoveAnnotations(), t.RemoveEllipses(), l.JsonSchema(ref=ref)
    )
    data = transformer.transform(tree)
    if resolve:
        resolve_refs(data)
    return data


def skema(tree,):
    transformer = TransformerChain(t.RemoveAnnotations(), l.Skema())
    data = transformer.transform(tree)
    return data


def python(tree):
    transformer = TransformerChain(
        t.RemoveAnnotations(),
        t.RemoveEllipses(),
        t.MergeIntersections(),
        t.Splitter(unions_inside_objects=False, unions_inside_lists=False),
        t.SortOptionalsLast(),
        l.Python(),
    )

    return transformer.transform(tree)


def typescript(tree):
    transformer = TransformerChain(
        t.RemoveAnnotations(),
        t.RemoveEllipses(),
        t.MergeIntersections(),
        t.Splitter(unions_inside_objects=False, unions_inside_lists=False, ),
        l.Typescript(),
    )
    return transformer.transform(tree)


def graphql(tree):
    transformer = TransformerChain(
        t.RemoveAnnotations(),
        t.RemoveEllipses(),
        t.MergeIntersections(),
        t.Splitter(),
        # t.Printer(),
        l.Graphql(),
    )

    return transformer.transform(tree)
