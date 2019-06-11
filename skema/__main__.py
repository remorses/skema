# printf "\nA:\n  b: Str\n" | xargs -0I%  python -m src %

from .tokenize import tokenize
from .make_schema import make_schema
from .make_tree import make_tree
import sys
import json
from functools import reduce, partial

rcompose = lambda *arr: reduce(lambda f, g: lambda *a, **kw: f(g(*a, **kw)), reversed(arr))

main = rcompose(
    tokenize,
    make_tree,
    make_schema,
    partial(json.dumps, indent=4)
)


string = sys.stdin.read()

# string = """
# Bot:
#     ciao: Str
# """

print(main(string))

# print(reduce(lambda a, b: a + b, reversed([1, 2])))

