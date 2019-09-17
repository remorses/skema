from .split_tree_parts import split_tree_parts
from .tree import Node


scalar_already_present = [ # empty to make tests pass
    'ID',
    # 'Json', 
    # 'DateTime',
    # 'Time',
    # 'Date',
]

def to_graphql(string: str, hide=scalar_already_present, only=None) -> str:
    refs = split_tree_parts(string, language='graphql', hide=hide, only=only,)
    if not 'Json' in hide and not (only and not 'Jons' in only):
        refs += [Node('Json',).append([Node('')])] 
    types = [t.to_graphql() for t in refs]
    schema = '\n\n'.join(types)
    return schema