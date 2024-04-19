from flask import Flask, jsonify
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