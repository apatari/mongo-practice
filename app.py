from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from config import app, client
from passCheck import pass_strong as isStrongPassword

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from email_validator import validate_email, EmailNotValidError

load_dotenv()

db = client.TEST_DB

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

    #unique name validation
    user = db.users.find_one({"name": json['name']})
    if user:
        return {"errors": ["Name already regeistered"]}, 422
    
    # email validation
    email = json['email']

    try:
        emailInfo = validate_email(email, check_deliverability=False)
        email = emailInfo.normalized
    
    except EmailNotValidError as err:
        # return the email error as a readable string
        return {"errors": [str(err)]}
    
    # verify password strength
    if len(json['password']) < 8:
        return {"errors:": ["Password must be 8 or more characters"]}, 422
    
    if not isStrongPassword(json['password']):
        return {"errors": ["Password must contain uppercase, lowercase, number, and special character"]}, 422

    # Password hashing
    hashed_password = generate_password_hash(json['password'])

    # Add the user to the db
    result = db.users.insert_one({
        'name': json['name'],
        'email': email,
        'password': hashed_password
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