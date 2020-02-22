import os
import os.path
import time
from bson import ObjectId
from flask import request, Blueprint, make_response, jsonify
from werkzeug.utils import secure_filename
from instances import app
from db_ops.transporter import write_to_db

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
        file_pathname = user_id + '.txt'
        filename = secure_filename(file_pathname)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #  time.sleep(.2)
        # call method to parse file and save it to the file db
        # XXX very risky business going on here, try to be safe!
        # removes all utf-8 encodings of unicode from file
        clean_file = "sed -i -e 's/\\xc2\\x91\|\\xc2\\x92\|\\xc2\\xa0\|\\xe2\\x80\\x8e//g' "
        clean_file = clean_file + 'file_ops/' + file_pathname
        print('clean file cmd: ', clean_file)
        os.system(clean_file)
        # now call go function to parse file and write to json
        go_func = './file_ops/main ' + 'file_ops/' + file_pathname
        print('go parse main cmd: ', go_func)
        os.system(go_func)
        # check if file was generated properly
        json_filename = 'file_ops/' + file_pathname + '.json'
        print('json filename: ', json_filename)
        #  time.sleep(.5)
        if not os.path.isfile(json_filename):
            print('json doesnt exist')
            resp = jsonify({'success': False, 'error' : 'Internal server error'})
            resp.status_code = 500
            return resp
        # now call method to parse the file into db
        try:
            write_to_db(json_filename, user_id)
        except Exception as e:
            print(e)
            resp = jsonify({'success': False, 'error' : 'Internal server error'})
            resp.status_code = 500
            return resp
        # once file is in db, call method to process it
        resp = jsonify({'success': True, 'message' : 'File successfully uploaded'})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'success': False, 'error' : 'Only .txt files are allowed'})
        resp.status_code = 400
        return resp
