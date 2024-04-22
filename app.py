from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from config import app, client

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

load_dotenv()

db = client.PRACTICE_DB

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



@app.route('/')
def home():
    return jsonify({"data": "hello world"})

@app.route('/users', methods=['POST'])
def users():
    json = request.get_json()

    result = db.users.insert_one({
        'name': json['name'],
        'age': json['age']
    })
    
    response = db.users.find_one({'_id': result.inserted_id})
    response['_id'] = str(response['_id'])

    return response, 201

@app.route('/users/<string:user_id>', methods=['PATCH'])
def users_update(user_id):
    json = request.get_json()
    try:
        user = {
            'name': json['name'],
            'age': json['age']
        }

        result = db.users.update_one({'_id': ObjectId(user_id)}, {"$set": user})

        response = db.users.find_one({'_id': ObjectId(user_id)})
        response['_id'] = str(response['_id'])

        return response, 201
    
    except Exception as err:
        return {"errors": [str(err)]}, 422



@app.route('/inv/<string:page_id>')
def page(page_id):
    
    # cursor = db.inventory.find({'_id': ObjectId(page_id)})
    # results = list(cursor)
    # if len(results) == 0:
    #     return {"errors": "Not found"}, 404
    # else:
    #     dict = results[0]
    #     response_body = {
    #         'item': dict['item'],
    #         'qty': dict['qty'],
    #         'size': dict['size'],
    #         "id": str(ObjectId(dict['_id']))
    #     }
        
    #     return response_body, 200
    try:
        result = db.inventory.find_one({'_id': ObjectId(page_id)})

    except:
        return {"errors": "Not found"}, 404
    
    if not result:
        return {"errors": "Not found"}, 404
    result['_id'] = str(result['_id'])
   
    return result, 200




if __name__ == '__main__': 
  
    app.run(debug = True) 