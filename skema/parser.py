from lark import Lark
from lark.indenter import Indenter
from lark.reconstruct import Reconstructor
from .logger import logger
from .lark import Tree
from populate import indent_to

tree_grammar = r"""
    start: (_NL* root_pair)+ _NL*

    scalar: "Str" -> type_str
        | "String" -> type_int
        | "Int" -> type_int
        | "Float" -> type_float
        | "Bool" -> type_bool
        | "Any" -> type_any
        | "null" -> literal_null
        | "true" -> literal_true
        | "false" -> literal_false
        | ESCAPED_STRING -> literal_string
        | SIGNED_INT -> literal_integer
        | NAME -> reference
        | /\/.*\// -> regex
        | (SIGNED_INT  | SIGNED_FLOAT) ".." (SIGNED_INT | SIGNED_FLOAT) -> bounded_range
        | (SIGNED_INT  | SIGNED_FLOAT) ".." -> low_bounded_range
        | ".." (SIGNED_INT  | SIGNED_FLOAT) -> high_bounded_range

    literal_ellipsis: "..."
    union: (value ("|" (scalar | list))+)
    intersection: value (("&" scalar)+ _NL | "&" _NL object)

    ?value: scalar
        | union

    _TRIPLE_QUOTE: "\"\"\""

    annotation: _TRIPLE_QUOTE _NL (/.+/ _NL)* _TRIPLE_QUOTE _NL

    root_pair: [annotation] NAME ":" (_NL object | value _NL | intersection | list _NL)
    required_pair: [annotation] NAME ":" (_NL object | intersection | value _NL | list _NL)
    optional_pair: [annotation] NAME "?:" (_NL object | intersection | value _NL | list _NL)

    list: "[" (_NL object | value) "]"

    object: _INDENT (required_pair | optional_pair)+ [literal_ellipsis _NL] _DEDENT

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
"""


class TreeIndenter(Indenter):
    NL_type = "_NL"
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = "_INDENT"
    DEDENT_type = "_DEDENT"
    tab_len = 4


parser = Lark(
    tree_grammar,
    parser="lalr",
    postlex=TreeIndenter(),
    lexer_callbacks={"COMMENT": lambda c: None},
    tree_class=Tree,
)


def parse(string):
    string = "\n".join([l for l in string.split("\n") if l.strip()])
    string = indent_to('', string)
    logger.debug(string)
    t = parser.parse(string + "\n")
    logger.debug(t.pretty())
    return t
