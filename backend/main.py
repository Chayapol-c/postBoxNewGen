from flask import Flask, request,jsonify
from flask_pymongo import PyMongo 
from os import path, environ
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
from time import time
from flask_cors import CORS

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['MONGO_URI'] = environ.get("MONGO_URL")
mongo = PyMongo(app)

userMongodb = mongo.db.user
trackMongodb = mongo.db.track
lockerUserMongodb = mongo.db.locker_status_postman
lockerPostmanMongodb = mongo.db.locker_status_user

def timestamp():
    fmt = '%Y-%m-%d %H:%M:%S'
    ts = time()
    currentTime = str(datetime.fromtimestamp(ts).strftime(fmt))
    return currentTime

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
        return {'result' : 'this user already exist'}

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

@app.route('/user_add_track', methods = ['POST'])  #user add trackID
def add_track():
    data = request.json
    
    data_insert = {
        'username': data['username'],
        'name': data['name'],
        'trackID': data['trackID'],
        'timestamp': 0
    }

    user_name = {'username': data['username']}
    cursor = userMongodb.find(user_name)

    output = []
    for ele in cursor:
        output = {
            'username': ele['username'],
        }

    if len(output) == 1:
        trackMongodb.insert_one(data_insert)
        return {'result' : 'add track successful'}
    else:
        return {'result' : 'unknown user'}

@app.route('/postman_track', methods = ['PATCH'])
def postman_track():
    data = request.json

    filt = {
        'trackID': data['trackID']
    }    

    cursor = trackMongodb.find(filt)

    output_user = []
    output_track = []
    for ele in cursor:
        output_track = {
            'trackID': ele['trackID'],
            'timestamp': ele['timestamp']
        }
        output_user = {
            'username': ele['username']
        }

    lockerUser = {'username': output_user['username']}

    update_track = {'$set': {'timestamp': timestamp()}}
    update_locker = {'$set': {'Lock_postman': False}}

    if len(output_track) == 0:
        return {'result': 'invalid trackID'}
    else:
        if(output_track['timestamp'] != 0):
            return {'result': 'this track already sent'}
        trackMongodb.update_one(filt, update_track)
        lockerPostmanMongodb.update_one(lockerUser, update_locker)
        return {'result': 'sent!'}
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)