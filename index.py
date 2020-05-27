import os
import sys
from flask import Flask, jsonify, request, make_response, send_from_directory
from dotenv import load_dotenv
load_dotenv()

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

import logger  

LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

PORT = os.environ.get('PORT')

#app = Flask(__name__)

from app import app 

@app.route('/')
def index():
    return "This is the main page."

@app.route('/ping', methods=['GET'])
def dummy_endpoint():
    """ Testing endpoint """
    return jsonify(data = 'Server running'),200

@app.errorhandler(404)
def not_found(error):
    """ error handler """
    LOG.error(error)
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
    """ error handler """
    LOG.error(error)
    return make_response(jsonify({'error': 'Method not allowed'}), 405)

@app.errorhandler(500)
def server_error(error):
    """ error handler """
    LOG.error(error)
    return make_response(jsonify({error}), 500)

@app.errorhandler(Exception)
def exception_handler(error):
    print("error",str(repr(error)))
    LOG.error(error)
    return make_response(jsonify(error = str(repr(error)) ), 500)
    #return "!!!!"  + str(repr(error))
    
#if __name__ == '__main__':
LOG.info('running in port: %s', os.environ.get('PORT'))
app.run(host='0.0.0.0', port=int(PORT))

#app.config['DEBUG'] = os.environ.get('ENV') == 'development'
 