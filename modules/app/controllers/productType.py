import os
from flask import request, jsonify
from app import app, mongo, flask_bcrypt, jwt
from app.schemas import validate_productType
import logger
from bson.objectid import ObjectId
import datetime
import json
from bson.json_util import dumps, loads
import boto3
from app.annotations import check_cognito_header, check_cognito_user


@app.route('/productTypes', methods=['GET', 'POST'])
@check_cognito_header()
@check_cognito_user()
def productTypes():
    if request.method == 'GET':
        query = request.args
        data = json.loads(dumps(mongo.db.productTypes.find()))
        #print("data",data)
        #print("len",len(data))
        return jsonify(data), 200
    if request.method == 'POST':
        data = validate_productType(request.get_json())
        if data['ok']:
            data = data['data']
            data["createdAT"] = datetime.datetime.utcnow()
            data["createdBy"] = request.tokenUserId
            mongo.db.productTypes.insert_one(data)            
            return jsonify({'message': 'productType created successfully!'}), 200
        else:
            return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400

@app.route('/productTypes/<id>', methods=['GET', 'DELETE','PUT'])
@check_cognito_header()
@check_cognito_user()
def productType(id):
    
    #print("id",id)
    #print("args",request.args)

    if request.method == 'GET':
        query = request.args
        data = mongo.db.productTypes.find_one({"_id":ObjectId(id)})
        #print("data",data)
        #print("len",len(data))
        return jsonify(data), 200
    
    if request.method == 'DELETE':
        db_response = mongo.db.productTypes.delete_one({"_id":ObjectId(id)})
        if db_response.deleted_count == 1:
            response = {'message': 'record deleted'}
        else:
            response = {'message': 'no record found'}
        return jsonify(response), 200

    if request.method == 'PUT':
        #data = request.get_json()
        data = validate_productType(request.get_json())
        if data['ok']:
            data = data['data']
            data["updatedAT"] = datetime.datetime.utcnow()
            data["updatedBy"] = request.tokenUserId   
            db_response = mongo.db.productTypes.update_one({"_id":ObjectId(id)}, {'$set':data})
            #print("response",db_response.matched_count)
            if db_response.matched_count > 0:            
                return jsonify({'message': 'record updated'}), 200
            else:
                return jsonify({'message': 'error on record updated'}), 400   
        else:
            return jsonify({'message': 'Bad request parameters: {}'.format(data['message'])}), 400

        

 