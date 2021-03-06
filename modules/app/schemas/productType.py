from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

productType_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "accountId":{
            "type": "string"
        }
    },
    "required": ["name", "accountId"],
    "additionalProperties": False
}


def validate_productType(data):
    try:
        validate(data, productType_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}