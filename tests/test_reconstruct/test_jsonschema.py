from skema.reconstruct import from_jsonschema
from graphql import build_schema
from ..support import *


def test_1():
    print()
    t = from_jsonschema(o3)
    print(t.pretty())
    print(gens.typescript(t))
    print(gens.graphql(t))


false = False
true = True
null = None
o1 = {
    "title": "Object",
    "description": "",
    "type": "object",
    "properties": {
        "xxx": {"type": "string", "description": ""},
        "yyy": {"description": ""},
    },
    "additionalProperties": false,
}

o2 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$ref": "#/definitions/SchemaTypeEnums",
    "definitions": {
        "SchemaTypeEnums": {
            "title": "SchemaTypeEnums",
            "description": "",
            "enum": [
                {"const": "string"},
                {"const": "array"},
                {"const": "object"},
                {"const": "number"},
                {"const": "boolean"},
                {"const": "integer"},
            ],
        },
        "SchemaType": {
            "title": "SchemaType",
            "description": "",
            "anyOf": [
                {"$ref": "#/definitions/SchemaTypeEnums"},
                {"type": "array", "items": {"$ref": "#/definitions/SchemaTypeEnums"}},
            ],
        },
        "Block": {
            "title": "Block",
            "description": "",
            "anyOf": [
                {"$ref": "#/definitions/GenericBlock"},
                {"$ref": "#/definitions/Enum"},
                {"$ref": "#/definitions/Object"},
                {"$ref": "#/definitions/Array"},
                {"$ref": "#/definitions/Constant"},
                {"$ref": "#/definitions/AllOf"},
                {"$ref": "#/definitions/AnyOf"},
                {"$ref": "#/definitions/OneOf"},
            ],
        },
        "Object": {
            "title": "Object",
            "description": "",
            "type": "object",
            "properties": {
                "type": {"$ref": "#/definitions/SchemaType", "description": ""},
                "properties": {"description": ""},
                "additionalProperties": {"description": ""},
            },
            "additionalProperties": false,
            "required": ["type", "properties", "additionalProperties"],
        },
        "GenericBlock": {
            "title": "GenericBlock",
            "description": "",
            "type": "object",
            "properties": {
                "type": {"$ref": "#/definitions/SchemaType", "description": ""}
            },
            "additionalProperties": false,
            "required": ["type"],
        },
        "Enum": {
            "title": "Enum",
            "description": "",
            "type": "object",
            "properties": {
                "enum": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/Block"},
                    "description": "",
                }
            },
            "additionalProperties": false,
            "required": ["enum"],
        },
        "Constant": {
            "title": "Constant",
            "description": "",
            "type": "object",
            "properties": {"const": {"type": "string", "description": ""}},
            "additionalProperties": false,
            "required": ["const"],
        },
        "AllOf": {
            "title": "AllOf",
            "description": "",
            "type": "object",
            "properties": {
                "allOf": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/Block"},
                    "description": "",
                }
            },
            "additionalProperties": false,
            "required": ["allOf"],
        },
        "AnyOf": {
            "title": "AnyOf",
            "description": "",
            "type": "object",
            "properties": {
                "anyOf": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/Block"},
                    "description": "",
                }
            },
            "additionalProperties": false,
            "required": ["anyOf"],
        },
        "OneOf": {
            "title": "OneOf",
            "description": "",
            "type": "object",
            "properties": {
                "oneOf": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/Block"},
                    "description": "",
                }
            },
            "additionalProperties": false,
            "required": ["oneOf"],
        },
        "Array": {
            "title": "Array",
            "description": "",
            "type": "object",
            "properties": {"items": {"$ref": "#/definitions/Block", "description": ""}},
            "additionalProperties": false,
            "required": ["items"],
        },
    },
}


o3 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$ref": "#/definitions/Bot",
    "definitions": {
        "Bot": {
            "title": "Bot",
            "description": "",
            "type": "object",
            "properties": {
                "_id": {
                    "$ref": "#/definitions/ObjectId",
                    "description": ""
                },
                "user_id": {
                    "$ref": "#/definitions/ObjectId",
                    "description": ""
                },
                "username": {
                    "type": "string",
                    "description": ""
                }
            },
            "additionalProperties": false,
            "required": [
                "_id",
                "user_id",
                "username"
            ]
        },
        "User": {
            "title": "User",
            "description": "",
            "type": "object",
            "properties": {
                "bot_id": {
                    "$ref": "#/definitions/ObjectId",
                    "description": ""
                },
                "name": {
                    "type": "string",
                    "description": ""
                },
                "surname": {
                    "type": "string",
                    "description": ""
                }
            },
            "additionalProperties": false,
            "required": [
                "bot_id",
                "name",
                "surname"
            ]
        },
        "MessageCampaign": {
            "title": "MessageCampaign",
            "description": "",
            "type": "object",
            "properties": {
                "_id": {
                    "$ref": "#/definitions/ObjectId",
                    "description": ""
                },
                "bot_id": {
                    "$ref": "#/definitions/ObjectId",
                    "description": ""
                },
                "messages": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": ""
                }
            },
            "additionalProperties": false,
            "required": [
                "_id",
                "bot_id",
                "messages"
            ]
        },
        "PostCampaign": {
            "title": "PostCampaign",
            "description": "",
            "type": "object",
            "properties": {
                "_id": {
                    "$ref": "#/definitions/ObjectId",
                    "description": ""
                },
                "bot_id": {
                    "$ref": "#/definitions/ObjectId",
                    "description": ""
                },
                "posts": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": ""
                }
            },
            "additionalProperties": false,
            "required": [
                "_id",
                "bot_id",
                "posts"
            ]
        },
        "Campaign": {
            "title": "Campaign",
            "description": "",
            "anyOf": [
                {
                    "$ref": "#/definitions/MessageCampaign"
                },
                {
                    "$ref": "#/definitions/PostCampaign"
                }
            ]
        },
        "EventWindow": {
            "title": "EventWindow",
            "description": "",
            "type": "object",
            "properties": {
                "value": {
                    "type": "number",
                    "multipleOf": 1.0,
                    "description": ""
                },
                "timestamp": {
                    "type": "number",
                    "multipleOf": 1.0,
                    "description": ""
                }
            },
            "additionalProperties": false,
            "required": [
                "value",
                "timestamp"
            ]
        },
        "Event": {
            "title": "Event",
            "description": "",
            "type": "object",
            "properties": {
                "_id": {
                    "$ref": "#/definitions/ObjectId",
                    "description": ""
                },
                "bot_id": {
                    "$ref": "#/definitions/ObjectId",
                    "description": ""
                },
                "type": {
                    "enum": [
                        {
                            "const": "like"
                        },
                        {
                            "const": "bo"
                        }
                    ],
                    "description": ""
                },
                "likes": {
                    "type": "number",
                    "multipleOf": 1.0
                },
                "timestamp": {
                    "type": "number",
                    "multipleOf": 1.0,
                    "description": ""
                }
            },
            "additionalProperties": false,
            "required": [
                "_id",
                "bot_id",
                "type",
                "timestamp"
            ]
        },
        "ObjectId": {
            "title": "ObjectId",
            "description": ""
        },
        "ID": {
            "title": "ID",
            "description": ""
        }
    }
}
