from lxml import html
import csv
from pymongo import MongoClient
import pymongoimport
import pandas as pd
import os
from pathlib import Path
import json

# Open TUI folder
path = Path('D:\\ComCore_Projects\\')


def import_content(csv_name, project):
    client = MongoClient('localhost', 27017)

    mng_db = client[project]
    collect_name = csv_name
    db_cm = mng_db[collect_name]
    print(mng_db.list_collection_names())
    # pymongoimport

    # # cdir = os.path.dirname(__file__)
    cdir = os.getcwd()
    file_res = os.path.join(cdir, (csv_name + '.csv'))
    # print(file_res)

    # csvFile = open(file_res,'r')
    # print(csvFile)
    # data = pd.read_csv('EngLogic Archive.csv')
    # print(data)
    # file= open(file_res,"r")
    with open(csv_name + '.csv', 'r') as csvFile:
        # reader = csv.reader(csvFile)
        # print(reader)
        # data = list()
        # for row in reader:
        #     print(row)
        #     data.append(row)

        # print(data)
        print(csvFile)
        dict_file = csv.DictReader(csvFile)
        for row in dict_file:
            print(row)
            db_cm.insert_one(row)

    # dict_reader = csv.DictReader(file)
    # print(dict_reader.fieldnames)
    # for row in dict_reader:
    #     print(row)

    # #for csvRow in dict_reader:
    # data = json.dumps([row for row in dict_reader])

    # print(data)
    # with open(file_res) as csvFile:
    #     csvReader = csv.DictReader(csvFile)
    # data = pd.read_csv(r"C:\\Users\\bantuv\\Desktop\\Python_ComCoreProjects\\EngLogic Archive.csv")
    # print(data)
    # data_json = json.loads(data.to_json(orient='records'))
    # db_cm.remove()
    # db_cm.insert(data_json)


def write_headers(csv_writer, div_parent, csv_name, proj_name):
    header_arr = []
    for head in div_parent.iter("th"):
        # print(head.text_content())
        header_arr.append(head.text_content())

    csv_writer.writerow(header_arr)

    for row in div_parent.iter("tr"):
        contentArr = []
        for element in row.iter("td"):
            contentArr.append(element.text_content())

        csv_writer.writerow(contentArr)

    print('done writing csv')
    import_content(csv_name, proj_name)


def read_project_report(file_path, proj_name):
    # root = html.parse("D:\ComCore_Projects\AdanaBM1\Report.html").getroot()
    root = html.parse(file_path + "\\Report.html").getroot()
    print(root)
    header_elements = root.xpath('//h3')
    # print(th_elements)
    for header in header_elements:
        if header.text_content() != 'System Information':
            print(header.text_content())
            div_parent = (header.getparent()).getparent()
            csv_file_name = header.text_content() + '.csv'
            with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                write_headers(writer, div_parent, header.text_content(), proj_name)
                # writeContents(writer,div_parent)


if __name__ == "__main__":
    for files in os.listdir(path):
        if os.path.isdir(os.path.join(path, files)) and files == 'AdanaBM1':
            print(os.path.join(path, files))
            read_project_report(os.path.join(path, files), files)
