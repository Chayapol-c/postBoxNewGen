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
        'username': data['username'],
        'password': data['password']
    }
    user_name = {'username': data['username']}
    cursor = userMongodb.find(user_name)

    output = []
    for ele in cursor:
        output = {
            'username': ele['username'],
            'password': ele['password']
        }

    if len(output) == 0:
        userMongodb.insert_one(data_insert)
        return {'result' : 'create successful'}
    else:
        return {'result' : 'this user already create'}

@app.route('/login', methods = ['GET'])  #login
def check_user():
    data = request.json
    filt = {
        'username': data['username'],
        'password': data['password']
        }

    cursor = userMongodb.find(filt)

    output = []
    for ele in cursor:
        output = {
            'username': ele['username'],
            'password': ele['password']
        }

    if len(output) == 0:
        return {'result': 'invalid username or password'}
    else:
        return {'result': 'login successful'}

@app.route('/status_locker', methods = ['GET']) #status
def locker_status():
    data = request.json
    status = data['lock']

    if status == True:
        return {'result': 'lock'}
    else:
        return {'result': 'unlock'}

@app.route('/user_add_track', methods = ['POST'])
def add_track():
    data = request.json
    
    data_insert = {
        'user': data['user'],
        'name': data['name'],
        'trackID': data['trackID']
    }

    user_name = {'user': data['user']}
    cursor = userMongodb.find(user_name)

    output = []
    for ele in cursor:
        output = {
            'user': ele['user'],
            'name': data['name'],
            'trackID': ele['trackID']
        }

    if len(output) == 0:
        trackMongodb.insert_one(data_insert)
        return {'result' : 'add track successful'}
    else:
        return {'result' : 'unknow user'}

@app.route('/postman_track', methods = ['GET'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)