from functools import wraps
from flask import request, jsonify
import boto3
import logger
import os
from app import mongo

cognito_client = boto3.client('cognito-idp')

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

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

                    #print("user got",response['UserAttributes'])

                    for element in response['UserAttributes']:

                        if element['Name'] == 'email':
                            request.TokenEmail = element['Value']
                        
                    rv = f(*args, **kwargs)
                    return rv

                except Exception as exc:
                    LOG.error(exc)
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
            data = mongo.db.users.find_one({"email":request.TokenEmail})
            if data != None:

                request.tokenUserId = data['_id']
                #print("data",request.tokenUserId)
            else:
                return jsonify({
                    'message': 'Invalid user'
                }), 403
                            
            rv = f(*args, **kwargs)
            return rv
        return decorated_function
    return decorator