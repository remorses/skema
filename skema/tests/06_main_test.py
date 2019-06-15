import json
from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
import pytest
from .data import strings
from .support import keys, values
from .. import compile
from .. import main




@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_mmain_no_refs_resolve(string):
    print(main(string))



@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_mmain(string):
    print(main(string, resolve=True))
