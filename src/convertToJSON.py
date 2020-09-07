try:
    from pymongo import MongoClient
    import pandas as pd
    import json
    import csv
except Exception as e:
    print("Some Modules are missing")


##for reference https://github.com/soumilshah1995/CSVtoMongoDB/blob/master/test.py

class MongoDB(object):

    def __init__(self, dB_name=None, collection_name=None):
        self.dB_name = dB_name
        self.collection_name = collection_name

        self.client = MongoClient("localhost", 27017)

        self.DB = self.client[self.dB_name]
        self.collection = self.DB[self.collection_name]

    def InsertData(self, path=None):
        """
        :param path: Path os csv File
        :return: None
        """
        self.collection.drop()

        df = pd.read_csv(path)
        data = df.to_dict('records')  # Convert to dictionary

        # self.collection.insert_one({"index": "system_info", "data": data}) # inesrt into DB

        self.collection.insert_many(data, ordered=False)
        print("All the Data has been Exported to Mongo DB Server .... ")


if __name__ == "__main__":
    mongodb = MongoDB(dB_name='ComProjects', collection_name='AdanaBM1.SysInfo')
    mongodb.InsertData(path="System Information.csv")

# import csv
# import json
# import os
#
# from pymongo import MongoClient
#
#
# # file_res = os.path.join(cdir, ('Disk Space.csv'))
# # print(file_res)
#
# def convert_csv_file(csv_file):
#     with open(csv_file, 'r') as f:
#         csv_name = os.path.splitext(csv_file)[0]
#
#         client = MongoClient('localhost', 27017)
#         mg_db = client['ComCore_Projects']
#         print(mg_db.list_collection_names())
#         db_collect = mg_db[csv_name]
#         db_collect.drop()
#         dict_file = csv.DictReader(f)
#         for row in dict_file:
#             db_collect.insert_one(row)
#
#
# directory = os.getcwd()
# for root, dirs, files in os.walk(directory):
#     # print(files)
#     for csvFile in files:
#         if csvFile.endswith('.csv'):
#             print(csvFile)
#             convert_csv_file(csvFile)
