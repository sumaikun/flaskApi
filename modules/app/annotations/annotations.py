from functools import wraps
from flask import request, jsonify
import boto3
cognito_client = boto3.client('cognito-idp')

def check_cognito_header():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization') 
            if token is None:
                return jsonify({
                    'message': 'Missing Authorization Header'
                }), 401
            else:
                
                try:

                    response = cognito_client.get_user(
                        AccessToken=token
                    )

                    #print("user got",response)

                    rv = f(*args, **kwargs)
                    return rv

                except Exception as exc:

                    return jsonify({
                    'message': 'Invalid token'
                }), 403
                
        return decorated_function
    return decorator

def check_cognito_user():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            #request.extraData = "something"
            rv = f(*args, **kwargs)
            return rv
        return decorated_function
    return decorator