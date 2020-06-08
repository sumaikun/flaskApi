from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

product_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
        },
        "collections":{
            "type": "array",
        },
        "productType":{
            "type": "string",
        },
        "tags":{
            "type": ["array", "null"]
        },
        "description": {
            "type": "string",
        },
        "sku": {
            "type": "string",
        },        
        "barcode": {
            "type": "string",
        },        
        "pricing": {
            "type": "string",
        },        
        "weight": {
            "type": "number",
        },        
        "media": {
             "type": ["array", "null"],
        },        
        "accountId": {
             "type": "string",
        }
    },
    "required": ["title", "collections", "productType", "sku", "pricing", "accountId","barCode"],
    "additionalProperties": False
}


def validate_product(data):
    try:
        validate(data, product_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}