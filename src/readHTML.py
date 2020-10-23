from lxml import html
import csv
from pymongo import MongoClient
import os
from pathlib import Path
from src.convertToJSON import MongoDBClass
from datetime import datetime

# Open TUI folder
path = Path('E:\\ComCore_Projects\\')

#variables to store the intermediate values
projArray = []
dateTimeDict = {}
backupsArray = []
contentArray = []

# Adding or updating project info into MongoDB
def insert_content(col_name, data, dataFilter, actionType):
    mongo_obj = MongoDBClass(dB_name='ComProjects', collection_name=col_name)
    if actionType == 'insert':
        mongo_obj.InsertData(data)
    elif actionType == 'update':
        mongo_obj.UpdateData(dataFilter, data)

# Writing Sys info content
def write_sytem_contents(div_parent, csv_name, proj_name):
    info_arr = []
    value_arr = []
    rest_update = False

    for row in div_parent.iter("tr"):
        for element in row.iter("td"):
            if element.text_content():                                                  ## check for empty strings
                if element.text_content().endswith(":"):
                    info_arr.append(element.text_content()[:-1])
                else:
                    value_arr.append(element.text_content())

    sys_info = dict(zip(info_arr, value_arr))
    project_id = sys_info['System Name'].lower()

    if sys_info['System Name'] in projArray:
        print(f'writing backups {sys_info["System Name"]}')
        backupsArray.append(sys_info)
        backup_date = datetime.strptime(sys_info['Date/Time (UTC)'], '%Y-%m-%d %X').date()
        #for date in dateTimeDict[sys_info['System Name']]:
        date = dateTimeDict[sys_info['System Name']]
        #print(f'date in array {date}')
        #print(f"date of file {backup_date}")
        if date < backup_date:
            dateTimeDict[sys_info['System Name']] = backup_date
            insert_content('Projects', {'Last Update on': str(backup_date)}, {'_id': project_id}, 'update')
            rest_update = True
    else:
        backupsArray.clear()
        #dateTimeDict.clear()
        proj_info = {key: sys_info[key] for key in sys_info.keys() & {'System Name', 'Operating System'}}               #https://www.geeksforgeeks.org/python-extract-specific-keys-from-dictionary/
        dict_info = {'_id': project_id, 'Project Name': proj_name, }
        dict_info.update(proj_info)
        projArray.append(sys_info['System Name'])
        insert_content('Projects', dict_info, '', 'insert')
        backupsArray.append(sys_info)
        last_date = datetime.strptime(sys_info['Date/Time (UTC)'], '%Y-%m-%d %X').date()
        dateTimeDict[sys_info['System Name']] = last_date
        print(f'date last update {dateTimeDict}')
        insert_content('Projects', {'Last Update on': str(last_date)}, {'_id': project_id}, 'update')
        rest_update = True

    backup_info = {'backups': backupsArray}
    insert_content('Projects', backup_info, {'_id': project_id}, 'update')

    return rest_update, project_id


#Adding other contents to the Database
def write_other_contents(div_parent, cont_type, proj_id):
    header_arr = []
    cont_arr = []
    contentArray.clear()

    for head in div_parent.iter("th"):
        header_arr.append(head.text_content())

    for row in div_parent.iter("tr"):
        cont_arr.clear()        #clearing the cont_arr so that the dictionary object can be created with same header keys
        for element in row.iter("td"):
            cont_arr.append(element.text_content())
        contentArray.append(dict(zip(header_arr,cont_arr)))

    if(len(contentArray) != 0):
        del contentArray[0]         # removing first empty object in content array
        content = {cont_type: contentArray}
        insert_content('Projects', content, {'_id': proj_id}, 'update')


def read_html_file(file_path, proj_name):
    root = html.parse(file_path).getroot()
    #print(file_path)
    #print(root)
    header_elements = root.xpath('//h3')
    update = False
    project_id = None
    # print(th_elements)
    for header in header_elements:
        doc_name = header.text_content().lower().replace(" ", "_")
        # adding system information
        if header.text_content() == 'System Information':
            div_parent = (header.getparent()).getparent()
            update, project_id = write_sytem_contents(div_parent, doc_name, proj_name)
        # adding the rest of the html content
        elif update:
            cont_type = header.text_content()
            div_parent = (header.getparent()).getparent()
            write_other_contents(div_parent, cont_type, project_id)


def read_other_file(file):
    print (f'in other file {file}')


def getFilePathInfo(absolute):
    basename = os.path.basename(absolute)
    info = os.path.splitext(basename)
    file_info = {
        "dirname": os.path.dirname(absolute),
        "basename": os.path.basename(absolute),
        "info": os.path.splitext(basename),
        "filename": info[0],
        "extend": info[1]
    }
    return file_info


def read_project_report(file_path, proj_name):
    if os.path.isfile(file_path):
        if(getFilePathInfo(file_path)["extend"] == ".html"):
            read_html_file(file_path, proj_name)
        else:
            read_other_file(file_path)


if __name__ == "__main__":
    for project in os.listdir(path):
        projName = project
        project = project.replace(" ","_")
        #print(f"project {project}")
        if os.path.isdir(os.path.join(path, project)):
            # print(os.listdir(os.path.join(path, project)))
            proj_path = os.path.join(path, project)
            for file in os.listdir(proj_path):
                file_path = os.path.join(proj_path,file)
                #if (project == "JacareiPM1"):
                read_project_report(file_path, projName)
