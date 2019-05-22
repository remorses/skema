
# print(json.dumps(tokens, indent=4))
# print(json.dumps([{t['type']: t['value']} for t in tokenizer], indent=4))
# print(make(tokens,))
from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
import json

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
if __name__ == "__main__":
  tokens = tokenize(schema)

  print(json.dumps(make_schema(make_tree(tokens),), indent=4))