
from lark import Lark
from lark.indenter import Indenter
from lark.reconstruct import Reconstructor

tree_grammar = r'''
    start: (_NL* pair)+ _NL*

    scalar: "Str" -> str
        | "Int" -> int
        | "Float" -> float
        | "Bool" -> bool
        | "null" -> null
        | "true" -> true
        | "false" -> false
        | ESCAPED_STRING -> literal_string
        | NAME -> ref
        | /\/.*\// -> regex
        | range
        | SIGNED_INT -> literal_int

    ellipsis: "..."
    union: value ("|" scalar)+
    intersection: value (("&" scalar)+ | "&" _NL object)

    ?range: (SIGNED_INT  | SIGNED_FLOAT) ".." (SIGNED_INT | SIGNED_FLOAT) -> bounded_range
        | (SIGNED_INT  | SIGNED_FLOAT) ".." -> low_bounded_range
        | ".." (SIGNED_INT  | SIGNED_FLOAT) -> high_bounded_range

    ?value: scalar
        | union
        | intersection

    _TRIPLE_QUOTE: "\"\"\""

    annotation: _TRIPLE_QUOTE _NL (/.+/ _NL)* _TRIPLE_QUOTE _NL


    ?pair: required_pair | optional_pair
    required_pair: [annotation] NAME ":" (_NL object | value _NL | list _NL)
    optional_pair: [annotation] NAME "?:" (_NL object | value _NL | list _NL)

    list: "[" (_NL object | value) "]"

    object: _INDENT pair* [ellipsis _NL] _DEDENT

    COMMENT: /#.*/

    %import common.CNAME -> NAME
    %import common.WS_INLINE
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.INT
    %import common.FLOAT
    %import common.SIGNED_INT
    %import common.SIGNED_FLOAT
    %declare _INDENT _DEDENT
    %ignore WS_INLINE
    %ignore COMMENT

    
    _NL: ["\r"] "\n" " "*
'''
# _NL: /(\r?\n[\t ]*)+/

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter(), lexer_callbacks={'COMMENT': lambda c: None})
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
