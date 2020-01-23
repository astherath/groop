#!/usr/bin/env python3
import word_trend
import pymongo
from flask import Flask, jsonify, request, make_response, url_for, send_file, render_template

# init flask app
app = Flask(__name__, template_folder='www')

# XXX dont forget to take this out in finished version
app.config['DEBUG'] = False

# default error response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# home response sends to index file
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return make_response(jsonify({'welcome!': 'Sucessful default connection'}), 200)

@app.route('/find', methods=['GET'])
def find_message():
    word = request.args.get('word')

    print(F'word: {word}')

    if word is None:
        return make_response(jsonify({'error': 'missing or invalid input'}), 400)

    word_trend.main_func(word)
    #  return '<img src=\"../www/plot.png\">'
    #  return app.send_static_file('../www/index.html')
    return make_response(jsonify({'welcome!': 'Sucessful default connection'}), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

