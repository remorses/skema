import pytest
import json
from ..fake_data import fake_data
from .. import to_jsonschema
from .support import values, keys
from jsonschema import validate

schemas = {
    'simple': """
    Root:
        a: Int
        b: Str
        c:
            x: Any
            y: Str | Int
""",
    'complex': """
Root: EventA & EventB
EventA:
    type: Str
    fields:
        args: [
            name: Str
            type: Str | Any
        ]
    ...

EventB:
    timestamp: Int
    sentBy: Str
    madeBy: "me" | "you"
    ...

""",
}

@pytest.mark.parametrize("string", values(schemas), ids=keys(schemas))
def test_fake_data(string):
    json_schema = to_jsonschema(string, resolve=True)
    # print(json_schema)
    fakes = fake_data(string)
    for o in fakes:
        print(json.dumps(o, indent=4, ensure_ascii=False))
        validate(o, json_schema, )
