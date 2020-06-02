from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

location_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "address":{
            "type": "string"
        },
        "locationProfile":{
            "type" : "string",
            "enum" : ["Warehouse", "Residential"]
        },
        "accountId":{
            "type": "string"
        }

    },
    "required": ["name", "address", "locationProfile", "accountId"],
    "additionalProperties": False
}


def validate_location(data):
    try:
        validate(data, location_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}