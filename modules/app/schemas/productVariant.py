from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

productType_schema = {
    "type": "object",
    "properties": {
        "option": {
            "type": "string",
        },
        "sku": {
            "type": "string",
        },
        "barCode":{
            "type": "string"
        },
        "weight": {
            "type": "number",
        },
        "productId": {
            "type": "string",
        },
        "media":{
            "type": ["string", "null"]
        },
        "accountId":{
            "type": "string"
        }
    },
    "required": ["sku", "barCode", "accountId"],
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