from .support import *

@pytest.mark.parametrize("x", schemas, ids=names)
def test_python(x):
    print(gens.python(parse(x)))

@pytest.mark.parametrize("x", schemas, ids=names)
def test_grpahql(x):
    print(gens.graphql(parse(x)))

@pytest.mark.parametrize("x", schemas, ids=names)
def test_jsonschema(x):
    pretty(gens.jsonschema(parse(x)))

@pytest.mark.parametrize("x", schemas, ids=names)
def test_typescript(x):
    print(gens.typescript(parse(x)))
