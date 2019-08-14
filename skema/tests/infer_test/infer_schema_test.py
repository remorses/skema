
from skema.infer import infer_schema
from skema.support import pretty

def test_1():
    x = infer_schema([
        {'steps': {'a': 5, 'b': 4}},
        {'steps': {'a': 'asd'}},
    ])

    pretty(x)