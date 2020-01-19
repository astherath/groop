from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo

# init flask app
app = Flask(__name__)

# XXX dont forget to take this out in finished version
app.config['DEBUG'] = True

# add mongo url to flask config, so that flask_pymongo can use it to make connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/gc_data'
mongo = PyMongo()
# actually init mongo now after going through the modules
mongo.init_app(app)

collection = mongo.db.messages

# default error response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# home response sends to index file
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return make_response(jsonify({'welcome!': 'Sucessful default connection'}), 200)

@app.route('/find/containing', methods=['GET'])
def find_message():
    author = request.args.get('author')
    keyword = request.args.get('keyword')

    if author is None or if keyword is None:
        return make_response(jsonify({'error': 'missing or invalid input'}), 400)

    response = collection.find({"Author": author,



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
