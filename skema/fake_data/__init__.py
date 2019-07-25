
from .. import to_jsonschema
from jsonschema import validate
import json
from typing import List
from hypothesis import given, settings
from .hypo_schema import get_generator






def fake_data(schema: str, ref=None, amount=5, cutom_types={}) -> List[dict]:
    json_schema=to_jsonschema(schema, ref=ref, resolve=True)
    examples = []
    @given(get_generator(json_schema, cutom_types))
    @settings(max_examples=amount)
    def generate(example_data):
        examples.append(example_data)
    generate()
    return examples


