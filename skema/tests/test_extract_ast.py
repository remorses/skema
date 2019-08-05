from ..make_tree import extract_ast, make_value_tree




def test_extract_ast():
    x = extract_ast('a &')
    x = list(x)
    print(x)