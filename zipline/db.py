from flask_pymongo import pymongo


class DatabaseCollection:
    """
    TODO: Add documentation
    """
    
    def __init__(self):
        self.__DB_CONNECTIONG_STRING = "mongodb+srv://app:uBtU55fMt0KLebrl@cluster0.afwwy.gcp.mongodb.net/greendeck?retryWrites=true&w=majority"
        self.__client = pymongo.MongoClient(self.__DB_CONNECTIONG_STRING)
        self.__db = self.__client.get_database('greendeck')
        self.collection = pymongo.collection.Collection(self.__db, 'greendeck')
    
    def get_collection(self):
        return self.collection