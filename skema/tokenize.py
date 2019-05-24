

from .parser import Tokenizer, EOF_TOKEN
import json

Tokenizer.__next__ = Tokenizer.get_next_token
Tokenizer.__iter__ = lambda self: iter(self.get_next_token, EOF_TOKEN)


def tokenize(string):
  tokenizer = Tokenizer(string)
  tokens = [t for t in tokenizer]
  while tokens[0]['type'] == 'SEPARATOR':
    tokens = tokens[1:]
  while tokens[-1]['type'] == 'SEPARATOR':
    tokens = tokens[:-1]
  return tokens

