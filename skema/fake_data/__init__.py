
from .. import to_jsonschema
from jsonschema import validate
import json
from typing import List
from hypothesis import given, settings
from .hypo_schema import generate_from_schema






def fake_data(schema: str, amount=5) -> List[dict]:
    json_schema=to_jsonschema(schema, resolve=True)
    examples = []
    @given(generate_from_schema(json_schema))
    @settings(max_examples=amount)
    def generate(example_data):
        examples.append(example_data)
    generate()
    return examples


