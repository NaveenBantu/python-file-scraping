try:
    import os
    import pandas as pd
    import glob
    from pathlib import Path
except Exception as e:
    print("Some Modules are missing")

class AnalyzeLogs(object):

    def __init__(self, csv_path=None, proj_path=None, fileName= None):
        extension = 'csv'
        self.all_filenames = [i for i in glob.glob(os.path.join(csv_path, '*.{}').format(extension))]
        print(self.all_filenames)

        # combine all files in the list
        self.header_names = ['Timestamp', ' CmpId', 'ClassId', 'ErrorId', 'InfoId', 'InfoText']
        self.content = [pd.read_csv(f, header=None, comment=';', names=self.header_names, skip_blank_lines=True, usecols=[0, 1, 2, 3, 4, 5], encoding='utf-8') for f in self.all_filenames]
        self.combined_csv = pd.concat(self.content, ignore_index=True)

        print(self.combined_csv['InfoText'].str.contains('Persistence').value_counts()[True])
        self.extract_problem_logs(self.combined_csv, fileName, proj_path)

    def extract_problem_logs(self, df=None, fileName=None, project_path=None):
        # prob_csv = df.loc[(df['ClassId']>1) & (df['ClassId']<=8)]
        prob_csv = df.loc[(df['ClassId'] == 8)]  # extracting all the exceptions
        print(len(prob_csv))

        #check if there are any exceptions and then add to the file.
        if(len(prob_csv) > 0) :
            prob_csv.to_csv(os.path.join(project_path, fileName + "_exceptions.csv"), index=False, encoding='utf-8-sig')


# testing the class
if __name__ == "__main__":
    print('inside main')
    path = Path('E:\\ComCore_Projects\\JacareiPM1\\4_10_2020_Logs\\RunLogic APP\\')
    fileName = "4_10_logs"
    analyzecsv = AnalyzeLogs(csv_path=path, fileName= fileName)
    print(analyzecsv.all_filenames)

# write the combined csv to a file
# combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
