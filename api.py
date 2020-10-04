from flask import Flask
from flask_restful import Resource, Api
from flask_pymongo import pymongo

application = Flask(__name__)
api = Api(application)

DB_CONNECTIONG_STRING = "mongodb+srv://app:uBtU55fMt0KLebrl@cluster0.afwwy.gcp.mongodb.net/greendeck?retryWrites=true&w=majority"
client = pymongo.MongoClient(DB_CONNECTIONG_STRING)
db = client.get_database('greendeck')
collection = pymongo.collection.Collection(db, 'greendeck')

class Test(Resource):
    def get(self):
        print(collection.find_one())
        return "Collecyion data read succesfully"

api.add_resource(Test, '/')

if __name__ == '__main__':
    application.run()
