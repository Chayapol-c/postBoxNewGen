from flask import Flask, request
from flask_pymongo import PyMongo
from datetime import datetime
from time import time
from flask_cors import CORS
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = environ.get("MONGO_URL")
mongo = PyMongo(app)

userMongodb = mongo.db.user
trackMongodb = mongo.db.track
lockerStatusMongodb = mongo.db.locker_status

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
        'password': data['password'],
        'ID_line': 0
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

@app.route('/user/track', methods = ['POST'])  #user add trackID
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

@app.route('/postman/track', methods = ['PATCH']) #postman sent
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

    update_track = {'$set': {'timestamp': timestamp()}}
    update_locker = {'$set': {'Lock_postman': False}}

    if len(output_track) == 0:
        return {'result': 'invalid trackID'}
    else:
        lockerUser = {'username': output_user['username']}
        if(output_track['timestamp'] != 0):
            return {'result': 'this track already sent'}
        trackMongodb.update_one(filt, update_track)
        lockerStatusMongodb.update_one(lockerUser, update_locker)
        return {'result': 'sent!'}
        
@app.route('/status', methods = ['GET']) #status 
def locker_status():
    user = request.args.get('user')
    username = {'username': user}
    cursor = lockerStatusMongodb.find(username)
    output = []

    for ele in cursor:
        output = {
            'Lock_postman': ele['Lock_postman'],
            'Lock_user': ele['Lock_user'],
        }
    
    print(len(output))

    if len(output) == 0:
        return {'result': 'invalid user'}

    return {
        'Lock_postman': output['Lock_postman'],
        'Lock_user': output['Lock_user']
    }
    
@app.route('/status/update', methods = ['POST']) #locker status update
def locker_update():
    data = request.json
    
    filt = {
        'username': data['username']
    }
    update_status = {'$set': {
        'Lock_postman': bool(data['Lock_postman']),
        'Lock_user': bool(data['Lock_user'])
        }
    }

    lockerStatusMongodb.update_one(filt, update_status)

    return {'result': 'update succesful'}

@app.route('/user/unlock', methods = ['PATCH']) #user unlock 
def user_locker_unlock():
    lineID = request.args.get('ID_line')

    filt = {'ID_line': lineID}
    cursor = userMongodb.find(filt)

    output_user = []

    for ele in cursor:
        output_user = {
            'username': ele['username']
        }
    user = {'username': output_user['username']}
    curosr_locker = lockerStatusMongodb.find(user)
    update_locker = {'$set': {'Lock_user': False}}

    lockerStatusMongodb.update_one(user, update_locker)

    return {'result': 'unlock'}

@app.route('/user/lock', methods = ['PATCH']) #user lock
def user_locker_lock(): 
    lineID = request.args.get('ID_line')

    filt = {'ID_line': lineID}
    cursor = userMongodb.find(filt)

    output_user = []

    for ele in cursor:
        output_user ={
            'username': ele['username']
        }
    user = {'username': output_user['username']}
    curosr_locker = lockerStatusMongodb.find(user)
    update_locker = {'$set': {'Lock_user': True}}

    lockerStatusMongodb.update_one(user, update_locker)

    return {'result': 'lock'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3001', debug=True)