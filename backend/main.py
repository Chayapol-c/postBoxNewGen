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
        'password': generate_password_hash(data['password'], method='sha256'),
        'ID_line': 0
    }

    user_name = {'username': data['username']}
    cursor = userMongodb.find_one(user_name)

    inser_data = {
        'username': user_name['username'],
        'Lock_postman': True,
        'Lock_user': True
    }

    if not cursor:
        userMongodb.insert_one(data_insert)
        lockerStatusMongodb.insert_one(inser_data)
        return {'result' : 'create successful'}
    else:
        return {'result' : 'this user already exist'}

@app.route('/login', methods = ['POST'])  #login
def check_user():
    data = request.json
    filt = {
        'username': data['username'],
        }
    cursor = userMongodb.find_one(filt)

    if not cursor:
        return {'result': 'invalid username'}
    if not check_password_hash(cursor['password'],data['password']):
        return {'result': 'wrong password'}
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
    cursor = userMongodb.find_one(user_name)
    track_id = {'trackID': data['trackID']}
    cursor_track = trackMongodb.find_one(track_id)

    if not cursor:
        return {'result': 'unknown user'}
    if cursor_track:
        return {'result': 'this track already added'}
    else:
        trackMongodb.insert_one(data_insert)
        return {'result' : 'add track successful'}

@app.route('/user/track', methods = ['GET']) #get user trackID
def get_track():
    user = request.args.get('user')

    filt ={
        'username': user
    }

    output = []
    cursor = trackMongodb.find(filt).sort('timestamp', -1)

    for ele in cursor:
        output.append({
            'username': ele['username'],
            'name': ele['name'],
            'trackID': ele['trackID'],
            'timestamp': ele['timestamp']
        })

    if len(output) == 0:
        return {'result': 'invalid username or mai mee track'}
    return {'result': output}

@app.route('/user/track', methods = ['DELETE']) #user delete track
def delete_track():
    data = request.json

    filt = {
        'trackID': data['trackID']
    } 

    cursor = trackMongodb.find_one(filt)
    output = []

    if not cursor:
        return {'result': 'mai mee track nee u'}
    else:
        filt_delete = {'trackID': cursor['trackID']}
        trackMongodb.delete_one(filt_delete)
        return {'result': 'delete successful'}

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

        url = 'https://exceed17.cpsk-club.xyz/message?user='+output_user['username']
        requests.get(url)
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

    if len(output) == 0:
        return {'result': 'invalid user'}

    return {
        'Lock_postman': output['Lock_postman'],
        'Lock_user': output['Lock_user']
    }

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

@app.route('/count', methods = ['GET'])
def count_date():
    username = request.args.get('user')
    m = request.args.get('m')
    filt = {'username': username}

    data = trackMongodb.find(filt).sort('timestamp')
    
    output = []
    for ele in data:
        if(str(ele['timestamp']) != '0'):
            output.append({
                'year': ele['timestamp'][0:4],
                'month': ele['timestamp'][5:7],
                'date': ele['timestamp'][8:10]
            })

    arr = np.zeros((12, 31))

    for a in output:
        arr[int(a['month'])][int(a['date'])] += 1

    result = []
    for i in range(31):
        if arr[int(m)][i] != 0:
            result.append(str(i)+","+str(arr[int(m)][i]))

    if len(result) == 0:
        return {'result': [{}]}
    else:
        return {'result': result}
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3001', debug=True)