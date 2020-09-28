import os
from pathlib import Path
import zipfile

# Open TUI folder
path = Path('T:\\')

# place all the extracted files in an Output folder
outPath = Path('D:\\ComCore_Projects\\')


def extract_zip_file(file, path_zip, proj_folder):
    os.chdir(path_zip)
    try:
        zf = zipfile.ZipFile(file)
        print(zf.getinfo('Report.html').date_time)
        print(zf.getinfo('Report.html').filename)

        proj_path = os.path.join(outPath, proj_folder)
        if not os.path.isdir(proj_path):
            os.mkdir(os.path.join(outPath, proj_folder))

        # The Python zipfile module provides the ability to reference the contents of a zip file via ZipInfo objects.
        # These are tied to individual archive entries, but not by filename. During extraction, you can pass either
        # an archive filename, or a ZipInfo object. If you alter the ZipInfo object’s filename attribute before
        # extraction, extract(zipinfo) will then use the new name for extraction, but extract the original data.
        rep_info = zf.getinfo('Report.html')
        rep_date_time = rep_info.date_time
        rep_info.filename = str(rep_date_time[2]) + '_' + str(rep_date_time[1]) + '_' + str(
            rep_date_time[0]) + '_' + rep_info.filename

        zf.extract(rep_info, proj_path)

    except (IOError, zipfile.BadZipfile) as e:
        print(e)
        pass

    except KeyError:
        pass


def get_zip_file(zip_path, proj_name):
    for root, dirs, all_files in os.walk(zip_path):
        # looping through all the subfolders in the root to extract the Zip files
        for zipFile in all_files:
            if zipFile.endswith('.zip'):
                # print(zipFile)
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
        # if ( files == "AdanaBM1"):
        search_zip_files(os.path.join(path, files), files.replace(" ","_"))
