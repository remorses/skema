
from .infer_schema import infer_schema
from .schema_to_tree import schema_to_tree, SchemaBlock


def infer_skema(data_array):
    schema = infer_schema(data_array)
    schema = SchemaBlock.make(schema)
    references = []
    t = schema_to_tree(schema, references=references)
    res = ''
    res += t.to_skema()
    for ref in references:
        res += '\n\n'
        res += ref.to_skema()
    res += '\n'
    return res