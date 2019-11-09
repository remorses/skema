from .support import *


@pytest.mark.parametrize("x", schemas, ids=names)
def test_1(x):
    code = gens.skema(parse(x))
    print(code)
    
