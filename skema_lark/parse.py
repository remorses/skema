
from lark import Lark
from lark.indenter import Indenter
from lark.reconstruct import Reconstructor

tree_grammar = r"""
    start: (_NL* pair)+ _NL*

    scalar: "Str" -> str
        | "Int" -> int
        | "Float" -> float
        | "Bool" -> bool
        | "null" -> null
        | "true" -> true
        | "false" -> false
        | ESCAPED_STRING -> literal_string
        | SIGNED_NUMBER -> literal_number
        | NAME -> ref

    union: value ("|" scalar)+
    intersection: value ("&" scalar)+

    ?value: scalar
        | union
        | intersection

    pair: NAME ":" (_NL object | value _NL | list _NL)

    list: "[" (_NL object | value) "]"

    object: _INDENT pair+ _DEDENT

    %import common.CNAME -> NAME
    %import common.WS_INLINE
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %declare _INDENT _DEDENT
    %ignore WS_INLINE

    
    _NL: ["\r"] "\n" " "*
"""
# _NL: /(\r?\n[\t ]*)+/

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter(), )
# reconstructor = Reconstructor(parser)

test_tree = """
a
    b
    c
        d
        e
    f
        g
"""

def test():
    t = parser.parse(test_tree)
    print(t.pretty())
    print(reconstructor.reconstruct(t))
