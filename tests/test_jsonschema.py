from .support import *
import fastjsonschema
from graphql import build_schema


@pytest.mark.parametrize("x", schemas, ids=names)
def test_schema_is_dumpable(x):
    code = gens.jsonschema(parse(x))
    pretty(code)
    json.dumps(code)

@pytest.mark.parametrize("x", schemas, ids=names)
def test_schema_valid(x):
    code = gens.jsonschema(parse(x))
    pretty(code)
    validate = fastjsonschema.compile(code)
    with pytest.raises(fastjsonschema.JsonSchemaException):
        validate(None)
    
