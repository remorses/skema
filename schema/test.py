

from parser import Tokenizer, EOF_TOKEN
from tree import dotdict, _make_tree, make, make_schema
import json

string_ = """
two:
  three: 3
  arr: [
    a: 1
    b: 2
    ...
  ]
four: 4
arr: [Str]
"""
string2 = """
obj:
  else: 2
  b: 2
  ...
  arr: [
    a: 1
    b: 3
    c: [
      a: Int
      c: s
      ...
      some: 
        ...
      shit: Str
    ]
  ]
  else: 2
"""
string3 = """
obj:
  else: 2
  b: 2
  c: 4
  e: 5
  b: 2
  c: 4
  e: 5

"""

Tokenizer.__next__ = Tokenizer.get_next_token
Tokenizer.__iter__ = lambda self: iter(self.get_next_token, EOF_TOKEN)


# print(json.dumps(tokens, indent=4))
# print(json.dumps([{t['type']: t['value']} for t in tokenizer], indent=4))
# print(make(tokens,))



# print(tokenizer.get_next_token())


schema = """
object:
  a: Int
  b: [Str]
  c: [
    a: Int
    b: Str
    ...
  ]
  some:
    shit:
      not: Cosa
"""
def tokenize(string):
  tokenizer = Tokenizer(string)
  tokens = [t for t in tokenizer]
  while tokens[0]['type'] == 'SEPARATOR':
    tokens = tokens[1:]
  while tokens[-1]['type'] == 'SEPARATOR':
    tokens = tokens[:-1]
  return tokens

if __name__ == "__main__":
  tokens = tokenize(schema)

  print(json.dumps(make_schema(make(tokens), ['Cosa']), indent=4))