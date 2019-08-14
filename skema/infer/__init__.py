
from genson import SchemaBuilder

from ..from_jsonschema import from_jsonschema, SchemaBlock
from ..support import pretty


def infer_schema(data_array, ):
    builder = SchemaBuilder()
    for data in data_array:
        builder.add_schema({"type": "object", "properties": {},})
        builder.add_object(data)
    schema = builder.to_schema()
    return schema

def infer_skema(data_array, ref_name='Root'):
    schema = infer_schema(data_array)
    return from_jsonschema(schema, ref_name=ref_name)
