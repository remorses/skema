
from skema.infer import infer_skema, infer_schema
from skema.support import pretty
import skema

def test_1():
    data = [
        {
            'tipo': 'experss',
            'cucchiaini': 34,
            'note': ['sdf', 'asd'],
            'camerieri': 34,
            'cosa': [{
                'ciao': 'sd',
                'sd': 9
            }]
        },
        {
            'tipo': 234,
            'camerieri': [{
                'nome': 'sdasd',
                'anni': 345
            }]
        }
    ]
    skema.tree.tab = '.   '
    x = infer_skema(data)
    print()
    print()
    print()
    print(x)
    x = x.replace('.', ' ')
    schema = skema.to_jsonschema(x)
    # pretty(infer_schema(data))
    # pretty(schema)