from genson import SchemaBuilder
from ..support import pretty


def infer_schema(data_array):
    builder = SchemaBuilder()
    for data in data_array:
        builder.add_schema({"type": "object", "properties": {},})
        builder.add_object(data)
    schema = builder.to_schema()
    return schema



