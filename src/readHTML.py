from lxml import html
import csv
from pymongo import MongoClient
import os
from pathlib import Path
from src.convertToJSON import MongoDBClass
from datetime import datetime

# Open TUI folder
path = Path('D:\\ComCore_Projects\\')

projArray = []
dateTimeArray = []
backupsArray = []
contentArray = []

# Adding or updating project info into MongoDB
def import_content(col_name, data, dataFilter, actionType):
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
        print(f'writing backups')
        backupsArray.append(sys_info)
        backup_date = datetime.strptime(sys_info['Date/Time (UTC)'], '%Y-%m-%d %X')
        for date in dateTimeArray:
            if date < backup_date:
                dateTimeArray[0] = backup_date
                rest_update = True
    else:
        backupsArray.clear()
        dateTimeArray.clear()
        proj_info = {key: sys_info[key] for key in sys_info.keys() & {'System Name', 'Operating System'}}               #https://www.geeksforgeeks.org/python-extract-specific-keys-from-dictionary/
        dict_info = {'_id': project_id, 'Project Name': proj_name}
        dict_info.update(proj_info)
        projArray.append(sys_info['System Name'])
        import_content('Projects', dict_info, '', 'insert')
        backupsArray.append(sys_info)
        dateTimeArray.append(datetime.strptime(sys_info['Date/Time (UTC)'], '%Y-%m-%d %X'))
        print(f'date time of backup {dateTimeArray}')
        rest_update = True

    backup_info = {'backups': backupsArray}
    import_content('Projects', backup_info, {'_id': project_id}, 'update')

    return rest_update, project_id


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
        import_content('Projects', content, {'_id': proj_id}, 'update')


def read_project_report(file_path, proj_name):
    root = html.parse(file_path).getroot()
    print(root)
    header_elements = root.xpath('//h3')
    update = False
    project_id = None
    # print(th_elements)
    for header in header_elements:
        doc_name = header.text_content().lower().replace(" ","_")
        if header.text_content() == 'System Information':
            div_parent = (header.getparent()).getparent()
            csv_file_name = doc_name+ '.csv'
            with open(csv_file_name, 'w', newline='', encoding='utf-8') as projFile:
                #writer = csv.writer(projFile)
                update, project_id = write_sytem_contents(div_parent, doc_name, proj_name)
        elif update:
            print(header.text_content())
            cont_type = header.text_content()
            #print(f'update value {update} of {project_id}')
            div_parent = (header.getparent()).getparent()
            csv_file_name = doc_name + '.csv'
            with open(csv_file_name, 'w', newline='', encoding='utf-8') as projFile:
                #writer = csv.writer(projFile)
                write_other_contents(div_parent, cont_type, project_id)
                # writeContents(writer,div_parent)


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
                #if (project == "AdanaBM1"):
                read_project_report(file_path, projName)

uniqueProjs = set(projArray)
projList = list(uniqueProjs)
projList.sort()
print(dateTimeArray)
