import json
from functools import reduce

log = lambda *x: None # print
# log = print

pretty = lambda x: print(json.dumps(x, indent=4, default=repr))

rcompose = lambda *arr: reduce(lambda f, g: lambda *a, **kw: f(g(*a, **kw)), reversed(arr))


def capitalize(s: str):
    if not s:
        return ''
    return s[0].capitalize() + s[1:]