from .support import *

@pytest.mark.parametrize("x", schemas, ids=names)
def test_python(x):
    print(gens.python(x))

@pytest.mark.parametrize("x", schemas, ids=names)
def test_grpahql(x):
    print(gens.graphql(x))

@pytest.mark.parametrize("x", schemas, ids=names)
def test_jsonschema(x):
    pretty(gens.jsonschema(x))

@pytest.mark.parametrize("x", schemas, ids=names)
def test_typescript(x):
    print(gens.typescript(x))
