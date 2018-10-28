from pymongo import MongoClient
from threading import Lock


# Singleton Class
class Database:
    db = None
    instance = None
    lock = Lock()

    def __init__(self, online):
        if online:
            MONGODB_URI = "mongodb://admin:csclassroom1@ds133762.mlab.com:33762/csclassroom"
            client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
            self.db = client.get_database("csclassroom")
        else:
            client = MongoClient('localhost', 27017)
            self.db = client.csclassroom


    @staticmethod
    def get_instance(online):
        Database.lock.acquire()
        if Database.instance is None:
            Database.instance = Database(online)
        Database.lock.release()
        return Database.instance


# Database Connection Online
db = Database.get_instance(online=True).db


# Database Connection Offline
'''
db = Database.get_instance(online=False).db
'''