import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://myAtlasDBUser:2704Mogo@myatlasclusteredu.slwycgi.mongodb.net/?retryWrites=true&w=majority&appName=myAtlasClusterEDU"


client = MongoClient(uri, server_api=ServerApi('1'))


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
    
