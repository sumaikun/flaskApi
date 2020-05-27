import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import datetime
import isodate as iso
from bson import ObjectId
from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter


class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return iso.datetime_isoformat(o)
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)


class ObjectIdConverter(BaseConverter):
    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)


# create the flask object
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('DB')
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=8)
mongo = PyMongo(app)
flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
#app.json_encoder = JSONEncoder
app.json_encoder = MongoJSONEncoder
app.url_map.converters['objectid'] = ObjectIdConverter
app.config['PROPAGATE_EXCEPTIONS'] = True

#app.config['AWS_DEFAULT_REGION'] = 'us-east'
#app.config['AWS_COGNITO_USER_POOL_ID'] = 'us-east-1_4TPzUCO9M'      


##unique indexes
mongo.db.users.create_index("email", unique=True)


from app.controllers import *  # pylint: disable=W0401,C0413