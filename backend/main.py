from flask import Flask, request,jsonify
from flask_pymongo import PyMongo 
from os import path, environ
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['MONGO_URI'] = environ.get("MONGO_URL")
mongo = PyMongo(app)

userMongodb = mongo.db.user
trackMongodb = mongo.db.track

@app.route('/create', methods = ['POST']) #create user
def create_user():
    data = request.json
    
    data_insert = {
        'user': data['user'],
        'name': data['name']
    }
    user_name = {'user': data['user']}
    cursor = userMongodb.find(user_name)

    output = []
    for ele in cursor:
        output = {
            'user': ele['user'],
            'name': ele['name']
        }

    if len(output) == 0:
        userMongodb.insert_one(data_insert)
        return {'result' : 'create successful'}
    else:
        return {'result' : 'this user already create'}

@app.route('/check', methods = ['GET'])
def check_user():
    user_name = request.args.get('User')
    filt = {'user': user_name}
    cursor = userMongodb.find(filt)

    output = []
    for ele in cursor:
        output = {
            'user': ele['user'],
            'name': ele['name']
        }

    if len(output) == 0:
        return {'result': 'the user name does not exist'}
    else:
        return {'result': 'found'}

@app.route('/status_locker', methods = ['GET'])
def locker_status():
    data = request.json
    status = data['lock']

    if status == True:
        return {'result': 'lock'}
    else:
        return {'result': 'unlock'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)