from .parse import parser
test_tree = """
a
    b
    c
        d
        e
    f
        g
"""

def test():
    t = parser.parse(test_tree)
    print(t.pretty())
    # print(reconstructor.reconstruct(t))

test()
