

from parser import Tokenizer, EOF_TOKEN
import json

string = """
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

Tokenizer.__next__ = Tokenizer.get_next_token
Tokenizer.__iter__ = lambda self: iter(self.get_next_token, EOF_TOKEN)

tokenizer = Tokenizer(string)

print(json.dumps([t for t in tokenizer], indent=4))



# print(tokenizer.get_next_token())








