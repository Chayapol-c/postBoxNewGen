from flask import Flask, request,jsonify
from flask_pymongo import PyMongo 

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_group17:9pd9akda@158.108.182.0:2255/exceed_group17'
mongo = PyMongo(app)

myCollection = mongo.db.test

@app.route('/create', methods = ['POST']) #create user
def create_user():
    data = request.json
    
    data_insert = {
        'user': data['user'],
        'name': data['name']
    }
    user_name = {'user': data['user']}
    cursor = myCollection.find_one(user_name)
    results = list(cursor)

    if len(results) == 0:
        myCollection.insert_one(data_insert)
        return {'result' : 'create successful'}
    else:
        return {'result' : 'this user already create'}

@app.route('/check', methods = ['GET'])
def check_user():
    user_name = request.args.get('User')
    
    user_name_data = myCollection.find(user_name_data)

    if not user_name_data:
        return {'result': 'found'}
    else:
        return {'result': 'the user name does not exist'}

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