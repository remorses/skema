

from .parser import Tokenizer, EOF_TOKEN
from functools import reduce
import json

Tokenizer.__next__ = Tokenizer.get_next_token
Tokenizer.__iter__ = lambda self: iter(self.get_next_token, EOF_TOKEN)


def remove_duplicates(acc, token):
  if acc and acc[-1]['type'] == 'SEPARATOR' and token['type'] == 'SEPARATOR':
    return acc
  else:
    return acc + [token]
   



def tokenize(string):
  tokenizer = Tokenizer(string)
  tokens = [t for t in tokenizer]
  tokens = reduce(remove_duplicates, tokens, [])
  if tokens[0]['type'] == 'SEPARATOR':
    tokens = tokens[1:]
  if tokens[-1]['type'] == 'SEPARATOR':
    tokens = tokens[:-1]
  return tokens

