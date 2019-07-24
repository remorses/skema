import pytest
import json
from ..fake_data import fake_data
from datetime import datetime
from .. import to_jsonschema
from .support import values, keys, log
from jsonschema import validate
import bson

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
    'datetime': """
    Ciao:
        x: /\d*/
        date: DateTime
        id: ObjectId
    
    DateTime: Any
    ObjectId: Any
    """
}

@pytest.mark.parametrize("string", values(schemas), ids=keys(schemas))
def test_fake_data(string):
    json_schema = to_jsonschema(string, resolve=True)
    # print(json_schema)
    fakes = fake_data(string)
    for o in fakes:
        print(json.dumps(o, indent=4, ensure_ascii=False))
        validate(o, json_schema, )

customs = {
    'DateTime': datetime.utcnow,
    'ObjectId': bson.ObjectId,
}

@pytest.mark.parametrize("string", values(schemas), ids=keys(schemas))
def test_fake_data_1(string):
    json_schema = to_jsonschema(string, resolve=True)
    log(json_schema)
    fakes = fake_data(string, cutom_types=customs)
    for o in fakes:
        print(json.dumps(o, indent=4, default=repr, ensure_ascii=False))
        validate(o, json_schema, )
