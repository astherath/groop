#!/usr/bin/env python3
import word_trend
import pymongo
from flask_cors import CORS
from user_ops.users import users
from file_ops.files import files
from instances import app
from flask import Flask, jsonify, request, make_response

# add folder to hold the files
UPLOAD_FOLDER = '/root/data_science_tests/file_ops'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# register blueprints
app.register_blueprint(users)
app.register_blueprint(files)

# enable CORS policy for flask instance
CORS(app)

# XXX dont forget to take this out in finished version
#  app.config['DEBUG'] = False
app.config['DEBUG'] = True

# default error response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# default index response sends 200
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return make_response(jsonify({'welcome!': 'Sucessful default connection'}), 200)

# plotting endpoint: takes in query word and raw data boolean, parses args then plots
@app.route('/find', methods=['GET'])
def find_message():
    word = request.args.get('word')
    raw = request.args.get('raw')
    raw = (raw == 'true')
    try:
        assert(word.isalnum())
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': 'No special characters allowed in query'}), 400)

    if word is None:
        return make_response(jsonify({'error': 'missing or invalid input'}), 400)

    # call actual plotting function that generates png and check for errors
    try:
        word_trend.main_func(word, raw) # XXX: maybe add pathname of file here?
    except:
        return make_response(jsonify({'Failure': 'Plot generated incorrectly'}), 500)
    # if no errors, send 200 ok
    return make_response(jsonify({'Success': 'Plot generated correctly'}), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, ssl_context=('/etc/letsencrypt/live/groop.pw/fullchain.pem', '/etc/letsencrypt/live/groop.pw/privkey.pem'))
