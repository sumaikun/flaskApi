import os
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from app import app, mongo, flask_bcrypt, jwt
from app.schemas import validate_user, validate_login
import logger
from bson.objectid import ObjectId
import datetime
import json
from bson.json_util import dumps, loads
import boto3
from app.annotations import check_cognito_header, check_cognito_user
#from app.helpers import checkSimpleForeign

user_pool_id = os.environ.get('COGNITO_POOL_ID')

client_id = os.environ.get('COGNITO_CLIENT_ID') 

cognito_client = boto3.client('cognito-idp')


ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'message': 'Missing Authorization Header'
    }), 401



@app.route('/AlternativeAuth', methods=['POST'])
def al_auth_user():
    ''' auth endpoint '''
    data = validate_login(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({'email': data['email']}, {"_id": 0})
        LOG.debug(user)
        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            access_token = create_access_token(identity=data)
            #refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token
            #user['refresh'] = refresh_token
            return jsonify({'data': user}), 200
        else:
            return jsonify({'message': 'invalid username or password'}), 401
    else:
        return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/auth', methods=['POST'])
def auth_user():

    data = validate_login(request.get_json())

    if data['ok']:
        data = data['data']

        auth_params = {'USERNAME':data['email'],
                    'PASSWORD':data['password']} 
        
        try:

            auth_response = cognito_client.admin_initiate_auth(UserPoolId=user_pool_id,
                                                            ClientId=client_id,
                                                            AuthFlow='ADMIN_NO_SRP_AUTH',
                                                            AuthParameters=auth_params)
            auth_json_response = json.dumps(auth_response)

            #print("auth_response",auth_json_response)

            #print("token",auth_response["AuthenticationResult"]["AccessToken"])

            return jsonify({"cognitoToken":auth_response["AuthenticationResult"]["AccessToken"]}), 200
        
        except Exception as exc:

            return jsonify({"message":"Auth error"}), 401
    else:
        return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400




@app.route('/registerFirstUser', methods=['POST'])
def register():
    ''' register user endpoint '''
    users = len(json.loads(dumps(mongo.db.users.find())))
    if len == 0:
        data = validate_user(request.get_json())
        if data['ok']:
            
            data = data['data']
            
            if data['password'] != None: 
                data['password'] = flask_bcrypt.generate_password_hash(
                    data['password'])
            data["createdAT"] = datetime.datetime.utcnow()            
            mongo.db.users.insert_one(data)
            return jsonify({'message': 'User created successfully!'}), 200
        else:
            return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400
    else:
        return jsonify({'message': 'can not created first user'}), 400


@app.route('/users', methods=['GET', 'POST'])
#@jwt_required
@check_cognito_header()
def users():
    ''' example to get extra data from annotation '''
    #print("extraData",request.extraData)
    ''' route read user '''
    if request.method == 'GET':
        query = request.args
        data = json.loads(dumps(mongo.db.users.aggregate([{'$addFields': {"_id": { '$toString':'$_id'}}}])))
        print("data",data)
        #print("len",len(data))
        return jsonify(data), 200
    if request.method == 'POST':
        data = validate_user(request.get_json())
        if data['ok']:
            data = data['data']
            if 'password' in data:
                data['password'] = flask_bcrypt.generate_password_hash(
                    data['password'])
            data["createdAT"] = datetime.datetime.utcnow()
            mongo.db.users.insert_one(data)
            return jsonify({'message': 'User created successfully!'}), 200
        else:
            return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@app.route('/users/<id>', methods=['GET', 'DELETE','PUT'])
@check_cognito_header()
#@jwt_required
def user(id):
    
    #print("id",id)
    #print("args",request.args)

    if request.method == 'GET':
        query = request.args
        data = mongo.db.users.find_one({"_id":ObjectId(id)})
        #print("data",data)       
        #print("len",len(data))
        
        """
        check = checkSimpleForeign("users",id)
        if check != True:
            return check
        """

        return jsonify(data), 200
    
    if request.method == 'DELETE':
        db_response = mongo.db.users.delete_one({"_id":ObjectId(id)})
        if db_response.deleted_count == 1:
            response = {'message': 'record deleted'}
        else:
            response = {'message': 'no record found'}
        return jsonify(response), 200

    if request.method == 'PUT':
        #data = request.get_json()
        data = validate_user(request.get_json())
        if data['ok']:
            data = data['data']
            if 'password' in data:            
                data['password'] = flask_bcrypt.generate_password_hash(
                    data['password'])
            data["updatedAT"] = datetime.datetime.utcnow()        
            db_response = mongo.db.users.update_one({"_id":ObjectId(id)}, {'$set':data})
            #print("response",db_response.matched_count)
            if db_response.matched_count > 0:            
                return jsonify({'message': 'record updated'}), 200
            else:
                return jsonify({'message': 'error on record updated'}), 400   
        else:
            return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400

        

 