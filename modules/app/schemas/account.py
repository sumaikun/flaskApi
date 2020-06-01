from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

account_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "userProfile":{
            "type" : "string",
            "enum" : ["Supplier", "Seller"]
        },
        "userId":{
            "type": "string"
        }

    },
    "required": ["name", "userType", "userId"],
    "additionalProperties": False
}


def validate_account(data):
    try:
        validate(data, account_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}