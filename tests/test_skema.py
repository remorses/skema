from .support import *


@pytest.mark.parametrize("x", schemas, ids=names)
def test_1(x):
    code = gens.skema(parse(x))
    print(code)

@pytest.mark.parametrize("x", schemas, ids=names)
def test_can_parse(x):
    code = gens.skema(parse(x))
    print(code)
    t = parse(code)
    print(t.pretty())
    
