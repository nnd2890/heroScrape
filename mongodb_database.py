import pymongo

class MongoDatabase:
    databaseName = "mydatabase"
    collectionName = "tripadvisor"

    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    def insertList(self, mylist):
        self.mydb = self.myclient[self.databaseName]
        self.mycol = self.mydb[self.collectionName]
        x = self.mycol.insert_many(mylist)
        print("Inserting... Finished! ",x.inserted_ids)