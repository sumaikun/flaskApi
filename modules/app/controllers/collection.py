import os
from flask import request, jsonify
from app import app, mongo, flask_bcrypt, jwt
from app.schemas import validate_collection
import logger
from bson.objectid import ObjectId
import datetime
import json
from bson.json_util import dumps, loads
import boto3
from app.annotations import check_cognito_header, check_cognito_user
from app.helpers import checkSimpleForeign


@app.route('/collections', methods=['GET', 'POST'])
@check_cognito_header()
@check_cognito_user()
def collections():
    if request.method == 'GET':
        query = request.args
        data = json.loads(dumps(mongo.db.collections.find()))
        #print("data",data)
        #print("len",len(data))
        return jsonify(data), 200
    if request.method == 'POST':
        data = validate_collection(request.get_json())
        if data['ok']:
            data = data['data']

            check = checkSimpleForeign("accounts",data['accountId'])
            if check != True:
                return check

            data["createdAT"] = datetime.datetime.utcnow()
            data["createdBy"] = request.tokenUserId
            mongo.db.collections.insert_one(data)            
            return jsonify({'message': 'collection created successfully!'}), 200
        else:
            return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@app.route('/collections/<id>', methods=['GET', 'DELETE','PUT'])
@check_cognito_header()
@check_cognito_user()
def collection(id):
    
    #print("id",id)
    #print("args",request.args)

    if request.method == 'GET':
        query = request.args
        data = mongo.db.collections.find_one({"_id":ObjectId(id)})
        #print("data",data)
        #print("len",len(data))
        return jsonify(data), 200
    
    if request.method == 'DELETE':
        db_response = mongo.db.collections.delete_one({"_id":ObjectId(id)})
        if db_response.deleted_count == 1:
            response = {'message': 'record deleted'}
        else:
            response = {'message': 'no record found'}
        return jsonify(response), 200

    if request.method == 'PUT':
        #data = request.get_json()
        data = validate_collection(request.get_json())
        if data['ok']:
            data = data['data']

            check = checkSimpleForeign("accounts",data['accountId'])
            if check != True:
                return check
                
            data["updatedAT"] = datetime.datetime.utcnow()
            data["updatedBy"] = request.tokenUserId   
            db_response = mongo.db.collections.update_one({"_id":ObjectId(id)}, {'$set':data})
            #print("response",db_response.matched_count)
            if db_response.matched_count > 0:            
                return jsonify({'message': 'record updated'}), 200
            else:
                return jsonify({'message': 'error on record updated'}), 400   
        else:
            return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400

        

 