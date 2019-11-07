import pytest
import json
from prtty import pretty
from skema.parser import parser, parse
import skema.languages as langs
import skema.transformers as trans
import skema.generators as gens
from .data import schemas, names


import json
import inspect
from operator import methodcaller
from functools import reduce
from funcy import compose


def get_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


class dotdict(dict):
    __getattribute__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


keys = compose(list, methodcaller("keys"))
values = compose(list, methodcaller("values"))

