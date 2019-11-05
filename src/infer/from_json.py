
from genson import SchemaBuilder
import json
from .from_jsonschema import from_jsonschema, SchemaBlock
from prtty import pretty

def replace_special_types(array):
    result = []
    inferrable_types = (dict, str, bool, int, float, list,)
    for obj in array:
        if isinstance(obj, (dict, list)):
            data = json.dumps(obj, default=str)
            result.append(json.loads(data))
        elif any([isinstance(obj, x) for x in inferrable_types]):
            result.append(obj)
    return result

def infer_schema(data_array, ):
    builder = SchemaBuilder()
    for data in data_array:
        builder.add_schema({"type": "object", "properties": {},})
        builder.add_object(data)
    schema = builder.to_schema()
    return schema

def infer_skema(data_array, ref_name='Root'):
    data_array = replace_special_types(data_array)
    schema = infer_schema(data_array)
    return from_jsonschema(schema, ref_name=ref_name)
