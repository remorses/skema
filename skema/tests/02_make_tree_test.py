
from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
from ..tree import map_tree, traverse_tree
import pytest
import fastjsonschema
from .data import strings
from .support import keys, values




@pytest.mark.parametrize("string", values(strings), ids=keys(strings))
def test_make_tree(string):
    tokens = tokenize(string)
    tree = make_tree(tokens)
    print(tree)
    result = traverse_tree(lambda x: x.value.strip(), tree)
    # print(result)
    # assert all(result)
    assert tree.children



# if __name__ == "__main__":
#     INDENT_SIZE = 4
#     tokens = tokenize(test_schema)
#     # print([t for t in tokens if t['value'] == 'Cosa'])
#     print(json.dumps(tokens, indent=4))
#     tree = make_tree(tokens)
#     print(tree)
#     print()
#     schema = make_schema(tree)
#     print(json.dumps(schema, indent=4))
#     schema['$ref'] = "#/definitions/Bot"
#     test_ = {
#         'username': "wow"
#     }
#     validate = fastjsonschema.compile(schema)
#     validate(test_)
#     print()

