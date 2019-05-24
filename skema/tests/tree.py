from .tree import Node, tree_from_dict


a = Node("1")
a \
    .insert(Node("2").insert(Node("2",))) \
    .insert(Node("3") \
        .insert(Node("4")
            .insert(Node("5").insert(Node("2",)))
        )
    ) \
    .insert(Node("6").insert(Node("2",)))

b = Node(1).insert(
        Node('&').insert(
            Node(2),
            Node(3)
        )
    )


t = tree_from_dict({
    'a': 1,
    'b': 2,
    'e': 1,
    'f': 2,
    'c': {
        'a': {
            'a': 1,
            'b': 2,
        },
        'b': 2,
    }
})