
from lark import Lark
from lark.indenter import Indenter
from lark.reconstruct import Reconstructor

tree_grammar = r'''
start: exp

terms: "a" | "b" | "c"

exp: exp "&" exp -> and
    | exp "|" exp -> or
    | terms

%import common.WS
%ignore WS
'''

tree_grammar = '''
start: exp

terms: "a" -> a
    | "b" -> b
    | "c"  -> c
    | "(" exp ")" -> group

?or: and | or ("|" and)+
?and: terms | and ("&" terms)+

?exp: or

%import common.WS
%ignore WS
'''
# _NL: /(\r?\n[\t ]*)+/

parser = Lark(tree_grammar, parser='lalr', )
# reconstructor = Reconstructor(parser)

test_tree = """
a & b & (c | a & a) & b & c 
"""

def test():
    t = parser.parse(test_tree)
    print(t.pretty())

test()
