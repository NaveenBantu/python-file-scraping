from lxml import html
import csv
from pymongo import MongoClient
import os
from pathlib import Path
from src.convertToJSON import MongoDBClass

# Open TUI folder
path = Path('D:\\ComCore_Projects\\')

projArray = []

def import_content(csv_name, col_name, data):
    # Adding every Sys info into MongoDB
    mongo_obj = MongoDBClass(dB_name='ComProjects', collection_name=col_name)
    mongo_obj.InsertData(data,csv_name)


def write_sytem_contents(csv_writer, div_parent, csv_name, proj_name):
    header_arr = ["Info", "Value"]
    csv_writer.writerow(header_arr)

    info_arr = []
    value_arr = []
    for row in div_parent.iter("tr"):
        for element in row.iter("td"):
            if element.text_content():                                                  ## check for empty strings
                if element.text_content().endswith(":"):
                    info_arr.append(element.text_content()[:-1])
                else:
                    value_arr.append(element.text_content())

    dict_info = dict(zip(info_arr,value_arr))

    projArray.append(dict_info['System Name'])
    print(dict_info['System Name'])

    #print(f'done writing csv {proj_name}')

    import_content(csv_name, 'SysInfo', dict_info)


def write_other_contents(csv_writer, div_parent, csv_name, proj_name):
    content_dict = {}
    header_arr = []
    for head in div_parent.iter("th"):
        # print(head.text_content())
        header_arr.append(head.text_content())

    csv_writer.writerow(header_arr)

    content_arr = []
    for row in div_parent.iter("tr"):
        for element in row.iter("td"):
            content_arr.append(element.text_content())

        #temp_dict = {**content_dict, **dict(zip(header_arr,content_arr))}
        #csv_writer.writerow(content_arr)

    dict_info = dict(zip(header_arr, content_arr))

    print(f'done writing csv {csv_name}')
    import_content(csv_name, csv_name, dict_info)


def read_project_report(file_path, proj_name):
    # root = html.parse("D:\ComCore_Projects\AdanaBM1\Report.html").getroot()
    root = html.parse(file_path).getroot()
    print(root)
    header_elements = root.xpath('//h3')
    # print(th_elements)
    for header in header_elements:
        doc_name = header.text_content().lower().replace(" ","_")
        if header.text_content() != 'System Information':
            print(header.text_content())
            div_parent = (header.getparent()).getparent()
            csv_file_name = doc_name + '.csv'
            with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                #write_other_contents(writer, div_parent, doc_name, proj_name)
                # writeContents(writer,div_parent)
        else:
            div_parent = (header.getparent()).getparent()
            csv_file_name = doc_name+ '.csv'
            with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                write_sytem_contents(writer, div_parent, doc_name, proj_name)


if __name__ == "__main__":
    for project in os.listdir(path):
        project = project.replace(" ","_")
        print(f"project {project}")
        if os.path.isdir(os.path.join(path, project)):
            # print(os.listdir(os.path.join(path, project)))
            proj_path = os.path.join(path, project)
            for file in os.listdir(proj_path):
                file_path = os.path.join(proj_path,file)
                # if (project == "AdanaBM1"):
                read_project_report(file_path, project)
