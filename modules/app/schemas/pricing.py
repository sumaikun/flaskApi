from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

pricing_schema = {
    "type": "object",
    "properties": {
        "price": {
            "type": "number",
        },
        "comparePrice":{
            "type": "number"
        },
        "costItem":{
            "type": "number"
        },
        "margin":{
            "type": "number"
        },
        "profit":{
            "type": "number"
        }
    },
    "required": ["price", "comparePrice", "costItem", "margin", "profit"],
    "additionalProperties": False
}


def validate_pricing(data):
    try:
        validate(data, pricing_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}