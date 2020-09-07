import csv
import json
import os

from pymongo import MongoClient


# file_res = os.path.join(cdir, ('Disk Space.csv'))
# print(file_res)

def convert_csv_file(csv_file):
    with open(csv_file, 'r') as f:
        csv_name = os.path.splitext(csv_file)[0]

        client = MongoClient('localhost', 27017)
        mg_db = client['AdanaBM1']
        print(mg_db.list_collection_names())
        db_collect = mg_db[csv_name]
        db_collect.drop()
        dict_file = csv.DictReader(f)
        for row in dict_file:
            db_collect.insert_one(row)


directory = os.getcwd()
for root, dirs, files in os.walk(directory):
    # print(files)
    for csvFile in files:
        if csvFile.endswith('.csv'):
            print(csvFile)
            convert_csv_file(csvFile)
