import json
import inspect
from operator import methodcaller
from functools import reduce

log = lambda x: print(json.dumps(x, indent=4, default=str, ensure_ascii=False))
def compose(*fs):
    """Composes passed functions."""
    if fs:
        pair = lambda f, g: lambda *a, **kw: f(g(*a, **kw))
        return reduce(pair, fs)
    

def get_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

class dotdict(dict):
    __getattribute__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

keys = compose(list, methodcaller('keys'))
values = compose(list, methodcaller('values'))