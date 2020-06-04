from app import app, mongo
from bson.objectid import ObjectId
from flask import request, jsonify

def checkSimpleForeign(collection,id):

    data = mongo.db[collection].find_one({"_id":ObjectId(id)})    
    if data is None:
        return jsonify({'message': 'invalid id for collection '+collection}), 400
    return True
