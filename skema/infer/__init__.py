
from .infer_schema import infer_schema
from .schema_to_tree import schema_to_tree, SchemaBlock


def infer_skema(data_array):
    schema = infer_schema(data_array)
