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
        "userRole": {
            "type": "string",
            "enum" : ["OWNER"]
        },
        "phone": {
            "type": "string",            
        },
        "cellPhone": {
            "type": "string",
            "minLength": 10,
            "maxlength":13
        },
        "accountId": {
            "type": "string",
        },
        "userProfile":{
            "type" : "string",
            "enum" : ["Supplier", "Seller"]
        }

    },
    "required": ["email", "name", "lastName", "documentType", "documentNumber", "userRole","userProfile"],
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