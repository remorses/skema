from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
from .data import strings
from .support import keys, values
import json
import pytest


@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_tokenize(string):
  tokens = tokenize(string)
  print(json.dumps(tokens, indent=4))
  assert tokens
  assert tokens[0]['value'] != 'SEPARATOR'
  assert tokens[-1]['value'] != 'SEPARATOR'
    

annotated = '''
"""ciao"""
Event:
    a: Int
    b: Str
"""ei"""
'''

def test_annotation():
  tokens = tokenize(annotated)
  print(json.dumps(tokens, indent=4))
  assert tokens[-1]['type'] == 'ANNOTATION'

# if __name__ == "__main__":
#   tokens = tokenize(schema)

#   print(json.dumps(make_schema(make_tree(tokens),), indent=4))