from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "lastName": {
            "type": "string",
        },
        "documentType": {
            "type" : "string",
            "enum" : ["CC", "CE","NIT"]
        },
        "documentNumber": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email",
        },
        "password": {
            "type": "string",
            "minLength": 5
        },
        "photoUrl": {
            "type": "string",
        },
        "role": {
            "type": "string",
        },
        "phone": {
            "type": "string",            
        },
        "cellPhone": {
            "type": "string",
            "minLength": 10,
            "maxlength":11
        },
        "accountId": {
            "type": "string",
        },
        "userType":{
            "type" : "string",
            "enum" : ["Supplier", "Seller"]
        }

    },
    "required": ["email", "name", "lastName", "documentType", "documentNumber", "role","userType"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}