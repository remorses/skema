
from skema.infer import infer_schema
from skema.support import pretty

def test_1():
    x = infer_schema([
        {'a': 3},
        {'b': 1.},
    ])

    pretty(x)