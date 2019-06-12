

from .parser import Tokenizer, EOF_TOKEN
from .support import log
from functools import reduce
import json

Tokenizer.__next__ = Tokenizer.get_next_token
Tokenizer.__iter__ = lambda self: iter(self.get_next_token, EOF_TOKEN)


def remove_duplicates(acc, token):
  if acc and acc[-1]['type'] == 'SEPARATOR' and token['type'] == 'SEPARATOR':
    return acc
  else:
    return acc + [token]
   

INDENT_SIZE = 4
def decompose_indents(acc, token):
  last = [x for x in acc if x['type'] == 'SEPARATOR']
  last = last[-1] if last else None
  if last and token['type'] == 'SEPARATOR':
    difference = (last['value'] - token['value']) // INDENT_SIZE
    if difference > 1:
      tokens = [token] * difference
      tokens = [{**x} for x in tokens]
      for i, token in enumerate(tokens):
        # print(last['value'] - ((i + 1) * INDENT_SIZE))
        tokens[i].update({'value': last['value'] - ((i + 1) * INDENT_SIZE)})
      return acc + tokens
    else:
      return acc + [token]
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
  tokens = reduce(decompose_indents, tokens, [])
  return tokens


if __name__ == "__main__":
    toks = [
      { 'value': 0 , 'type': 'SEPARATOR' },
      { 'value': 8 , 'type': 'SEPARATOR' },
      { 'value': 0 , 'type': 'SEPARATOR' },
    ]
    x = reduce(decompose_indents, toks, [])
    log(x)