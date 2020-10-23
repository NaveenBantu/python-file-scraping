import os
from pathlib import Path
import zipfile

from src.combine2 import AnalyzeLogs

# Open TUI folder
path = Path('T:\\')

# place all the extracted files in an Output folder
outPath = Path('E:\\ComCore_Projects\\')

def extract_log_files(zf, project_path, zip_name):
    rep_info = zf.getinfo('Report.html')
    rep_date_time = rep_info.date_time
    listOfFileNames = zf.namelist()

    log_folder = zip_name + '_Logs'
    log_path = os.path.join(project_path, log_folder)
    parent_log_folder = None

    for fileName in listOfFileNames:
        if fileName.endswith('.csv'):
            # Extract a single file from zip
            # zf.extract(fileName, 'temp_py')
            if ((fileName).find('APP') > -1):
                if not os.path.isdir(log_path):
                    os.mkdir(os.path.join(project_path, log_folder))

                zf.extract(fileName, log_path)
                print(f'All the csv files are extracted+ {log_path} {fileName} {rep_date_time}')
                parent_log_folder = fileName.split('/')[0]

    print(f'parent log folder {parent_log_folder}')
    if(parent_log_folder != None):
        csv_log_path = os.path.join(log_path, parent_log_folder)
        csv_log_analysis = AnalyzeLogs(csv_path=csv_log_path, proj_path=project_path, fileName=log_folder)


def extract_zip_file(file, path_zip, proj_folder):
    os.chdir(path_zip)
    try:
        zf = zipfile.ZipFile(file)

        proj_path = os.path.join(outPath, proj_folder)
        if not os.path.isdir(proj_path):
            os.mkdir(os.path.join(outPath, proj_folder))

        # The Python zipfile module provides the ability to reference the contents of a zip file via ZipInfo objects.
        # These are tied to individual archive entries, but not by filename. During extraction, you can pass either
        # an archive filename, or a ZipInfo object. If you alter the ZipInfo object’s filename attribute before
        # extraction, extract(zipinfo) will then use the new name for extraction, but extract the original data.
        rep_info = zf.getinfo('Report.html')

        # setting the filename in the folder
        zip_name = file.split(".")[0]
        rep_info.filename = zip_name + '_' + rep_info.filename

        zf.extract(rep_info, proj_path)
        extract_log_files(zf, proj_path, zip_name)

    except (IOError, zipfile.BadZipfile) as e:
        print(e)
        pass

    except KeyError as e1:
        print(e1)
        pass


def get_zip_file(zip_path, proj_name):
    for root, dirs, all_files in os.walk(zip_path):
        # looping through all the subfolders in the root to extract the Zip files
        for zipFile in all_files:
            if zipFile.endswith('.zip'):
                #print(root)
                extract_zip_file(zipFile, root, proj_name)          #changed the path of the zip file to the root of the os.walk (before it was pointing to the main folder)


def search_zip_files(path_sub, proj_name):
    for subFile in os.listdir(path_sub):
        if os.path.isdir(os.path.join(path_sub, subFile)):
            get_zip_file(os.path.join(path_sub, subFile), proj_name)
        elif subFile.endswith('.zip'):
            print(subFile)
            extract_zip_file(subFile, path_sub, proj_name)


for files in os.listdir(path):
    if os.path.isdir(os.path.join(path, files)):
        # print(files)

        #if (files == "JacareiPM1"):
        if (files != "CordobaPM1"):
            search_zip_files(os.path.join(path, files), files.replace(" ","_"))
