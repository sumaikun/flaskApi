from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

address_schema = {
    "type": "object",
    "properties": {
        "city": {
            "type": "string",
        },
        "country":{
            "type": "string"
        },
        "province":{
            "type": "string"
        },
        "provinceCode":{
            "type": "string"
        },
        "countryCode":{
            "type": "string"
        },
        "zip":{
            "type": "string"
        },
        "address":{
            "type": "string"
        },
        "addressSecondary":{
            "type": "string"
        },
        "phone":{
            "type": "string"
        },
        "cellPhone":{
            "type": "string"
        }
    },
    "required": ["city", "country", "address", "phone"],
    "additionalProperties": False
}


def validate_address(data):
    try:
        validate(data, address_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}