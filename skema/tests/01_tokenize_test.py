from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
import json
import pytest



many_props = """
X:
  a: 1
  b: 2
  c: 3
  d: 4
"""


very_deep = """
X:
  a: 1
    b: 2
      c: 3
        d: 4
          e: 5
"""
with_lines = """
Bot:
    username: "ciao"

Url: Str

Cosa:
    a: Str
    b: Str

"""

@pytest.mark.parametrize("string", [many_props, very_deep, with_lines], ids=lambda a: str(a))
def test_tokenize(string):
  tokens = tokenize(string)
  print(json.dumps(tokens, indent=4))
  assert tokens
  assert tokens[0]['value'] != 'SEPARATOR'
  assert tokens[-1]['value'] != 'SEPARATOR'
    

# if __name__ == "__main__":
#   tokens = tokenize(schema)

#   print(json.dumps(make_schema(make_tree(tokens),), indent=4))