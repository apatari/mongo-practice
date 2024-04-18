from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from config import app, client

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
load_dotenv()



# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



@app.route('/')
def home():
    return jsonify({"data": "hello world"})

if __name__ == '__main__': 
  
    app.run(debug = True) 