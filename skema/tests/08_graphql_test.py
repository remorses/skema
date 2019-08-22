import pytest
import json
from ..fake_data import fake_data
from datetime import datetime
from .. import to_jsonschema
from .support import values, keys, log
from jsonschema import validate
import bson

schemas = {
    '1': """
    Root:
        _id: ObjectId
        status: CampaignStatus
        byBusinessUserId: ObjectId
        name: String
        type: CampaignType
        costInCents: Int
        prsCount: [
            x: Int
        ]
        daysDuration: Int
        startedAt: DateTime
        deadline: DateTime
        campaignPrFilter: PrFilter
        prPartecipantsCount: Int

    ObjectId: Any
    PrFilter:
        bo: Int
        x: String
    CampaignType: "sdfg"
    CampaignStatus: Int
    DateTime: Any
    """
}

@pytest.mark.parametrize("string", values(schemas), ids=keys(schemas))
def test_1(string):
    json_schema = to_jsonschema(string, resolve=True)
    log(json_schema)
