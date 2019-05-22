
from ..tokenize import tokenize
from ..make_schema import make_schema
from ..make_tree import make_tree
import pytest
import fastjsonschema

simple = """
X:
    ciao: Str
    b: Int
"""
complex_schema = """
Bot:
    username: "ciao"
    data:
        competitors: [Str]
    dependencies: [Url]
Url: Str
Cosa:
    a: Str
    b: Str
    c: Int
    d:
        cosa: Cosa
        a: Int
        b: Int

"""

@pytest.mark.parametrize('string', [simple, complex_schema])
def test_make_tree(string):
    tokens = tokenize(string)
    tree = make_tree(tokens)
    assert tree
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

