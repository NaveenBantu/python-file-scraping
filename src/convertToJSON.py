try:
    from pymongo import MongoClient
    import pandas as pd
    import json
    import csv
except Exception as e:
    print("Some Modules are missing")


##for reference https://github.com/soumilshah1995/CSVtoMongoDB/blob/master/test.py

class MongoDBClass(object):

    def __init__(self, dB_name=None, collection_name=None):
        self.dB_name = dB_name
        self.collection_name = collection_name

        self.client = MongoClient("localhost", 27017)

        self.DB = self.client[self.dB_name]
        self.collection = self.DB[self.collection_name]

        #if self.collection:
         #   self.collection.drop()

    def InsertData(self, data=None):
        """
        :param path: Path os csv File
        :return: None
        """
        #self.collection.drop()
        # {doc_name: data}
        self.collection.insert_one(data)             #insert Dict type data into MongoDB Collection
        #print("All the Data has been Exported to Mongo DB Server .... ")

    def UpdateData(self, projFilter=None, data=None):
        self.collection.update_one(projFilter, {"$set": data})
        #print("updating data ")


if __name__ == "__main__":
    mongodb = MongoDBClass(dB_name='ComProjects', collection_name='project')                #test MongoDBClass
