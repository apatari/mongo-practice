from dotenv import load_dotenv
import os

from config import client

if __name__ == '__main--':
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    

