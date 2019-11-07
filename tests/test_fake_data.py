from skema.fake_data import fake_data
from jsonschema import validate
from .support import *
from datetime import datetime


customs = {
    'DateTime': datetime.utcnow,
    # 'ObjectId': bson.ObjectId,Ò
}

@pytest.mark.parametrize("string", schemas, ids=names)
def test_fake_data(string):
    json_schema = gens.jsonschema(parse(string), resolve=True)
    pretty(json_schema)
    fakes = fake_data(string, amount=30)
    for o in fakes:
        print(json.dumps(o, indent=4, ensure_ascii=False))
        validate(o, json_schema, )

