import os
from bson import ObjectId
from flask import request, Blueprint, make_response, jsonify
from werkzeug.utils import secure_filename
from instances import app

files = Blueprint('files', __name__)

@files.route('/files/upload', methods=['POST'])
def upload_file():
    # get username
    user_id = request.args.get('id')
    # turn id to bson
    try:
        _id = ObjectId(user_id)
        assert(_id is not None)
    except Exception as e:
        print('exception at id parsing')
        print(e)
        resp = jsonify({'success': False, 'error': 'Invalid user token'})
        resp.status_code = 400
        return resp
    print(request.files)
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'success': False, 'error' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'success': False, 'error' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and file.filename[-3:] == 'txt':
        filename = secure_filename(user_id + '.txt')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # call method to parse file and save it to the file db


        # once file is in db, call method to process it

        resp = jsonify({'success': True, 'message' : 'File successfully uploaded'})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'success': False, 'error' : 'Only .txt files are allowed'})
        resp.status_code = 400
        return resp
