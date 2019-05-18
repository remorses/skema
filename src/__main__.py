import poyo


class Node:
    def __init__(self, value, is_key=True):
        self.value = value
        self.is_key = is_key
        self.children = []
    
    def insert(self, node):
        self.children.append(node)
        return self
    
    def __repr__(self, indent=''):
        res = (indent + str(self.value))
        res += ':' if self.is_key else ''
        for c in self.children:
            if c.is_key:
                res += '\n' + Node.__repr__(c, indent + '\t')
            else:
                res += ' ' + str(c.value )
        return res



def make_tree(obj, key='root'):
    node = Node(key)
    for k, val in obj.items(): # properties
        if isinstance(val, dict): # is_object
            node.insert(make_tree(val, k))
        else:
            node.insert(Node(k,)).insert(Node(val, is_key=False))
    return node





# def _make_tree(string: str, key='root'):
#     node = Node(key)
#     if ':' in string:
#         k_end = string.index(':')
#         k = string[0:k_end]
#         node.insert(Node(k))
#         node.insert
#     else:
#         node.insert(Node(string.strip(), is_key=False)

#         for k, val in obj.items():
#             if isinstance(val, dict):
#                 node.insert(make_tree(val, k))
#             else:
#                 node.insert(Node(k,)).insert(Node(val, is_key=False))
#         return node




a = Node("1")
a \
    .insert(Node("2")).insert(Node("2", is_key=False)) \
    .insert(Node("3") \
        .insert(Node("4")
            .insert(Node("5")).insert(Node("2", is_key=False))
        )
    ) \
    .insert(Node("6")).insert(Node("2", is_key=False))


t = make_tree({
    'a': 1,
    'b': 2,
    'c': {
        'a': {
            'a': 1,
            'b': 2,
        },
        'b': 2,
    }
})

print(t)