from flask_pymongo import pymongo


class DatabaseCollection:
    """
    Common interface class to interact with MongoDB Cluster
    ---
    params:
        url: URL of the cluster, should contain username and password
        db: Database to connected to
        collection: Collection to connect to
    """
    
    def __init__(self, 
                    url='mongodb+srv://app:uBtU55fMt0KLebrl@cluster0.afwwy.gcp.mongodb.net/greendeck?retryWrites=true&w=majority', 
                    db='greendeck', collection='greendeck'):
        self.__DB_CONNECTIONG_STRING = url
        self.__client = pymongo.MongoClient(self.__DB_CONNECTIONG_STRING)
        self.__db = self.__client.get_database(db)
        self.collection = pymongo.collection.Collection(self.__db, collection)
    
    def get_collection(self):
        return self.collection