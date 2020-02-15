import os
from flask import request, Blueprint, make_response, jsonify
from werkzeug.utils import secure_filename
from instances import app

files = Blueprint('files', __name__)

@files.route('/files/upload', methods=['POST'])
def upload_file():
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
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'success': True, 'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'success': False, 'error' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp
