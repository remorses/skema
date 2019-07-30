

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

def remove_very_sames(acc, token):
  if acc and acc[-1]['type'] == 'SEPARATOR' and token['type'] == 'SEPARATOR' and acc[-1]['value'] == token['value']:
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
        value = last['value'] - ((i + 1) * INDENT_SIZE)
        tokens[i].update({'value': value})
      return acc + tokens
    else:
      return acc + [token]
  else:
    return acc + [token]

# TODO can get INDENT SIZE here
def get_base_level(acc, token):
  if token['type'] == 'SEPARATOR':
    base = min(acc['base'], acc['tokens'][-1]['start_column'])
  else:
    base = acc['base']
  return {
    'tokens': acc['tokens'] + [token],
    'base': base
  }


def tokenize(string):
  tokenizer = Tokenizer(string)
  tokens = [t for t in tokenizer]
  tokens = reduce(remove_duplicates, tokens, [])
  if tokens[0]['type'] == 'SEPARATOR':
    tokens = tokens[1:]
  if tokens[-1]['type'] == 'SEPARATOR':
    tokens = tokens[:-1]
  tokens = reduce(decompose_indents, tokens, [])
  base = reduce(get_base_level, tokens, {'tokens': [], 'base': 900,})['base']
  tokens = [t for t in tokens if not (t['type'] == 'SEPARATOR' and t['value'] < base)]
  tokens = reduce(remove_very_sames, tokens, [])
  return tokens



if __name__ == "__main__":
    toks = [
      { 'value': 0 , 'type': 'SEPARATOR' },
      { 'value': 8 , 'type': 'SEPARATOR' },
      { 'value': 0 , 'type': 'SEPARATOR' },
    ]
    x = reduce(decompose_indents, toks, [])
    log(x)