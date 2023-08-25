import json
import sys
from datetime import datetime, timedelta
from util import *

#TODO: add full path before folders
input_folder = 'clinical_trials_code/'
output_folder = 'internal_files/'


def fill_dict(data, Dict, years_ago, accepted_study_types):
    for key, value in data.items():
        device_num = value[0]
        for i in range(1, device_num + 1):
            end_date = (datetime.strptime(value[i][5], '%B %Y') if ',' not in value[i][5] else datetime.strptime(value[i][5], '%B %d, %Y'))
            enrollment = value[i][2]
            if enrollment == None:
                enrollment = 0
            else:
                enrollment = int(enrollment)
            study_type = value[i][3]
            if end_date >= years_ago and enrollment >= 50 and study_type in accepted_study_types:
                current_trial = [value[i][0], value[i][1], value[i][9]]
                if current_trial not in Dict[key]:
                    Dict[key].append(current_trial)
                    Dict[key][0] += 1
    return Dict


def filter(inputFile):
    outputFile = f'{output_folder + inputFile[4:-5]}.json'
    with open(input_folder + inputFile, encoding = 'utf8') as JSONFILE:
        data = json.load(JSONFILE)
        Dict = {}
        for key in data:
            Dict.update({key : [0]})
        #Completed
        years_ago = datetime.now() - timedelta(days = 5 * 365) #five years
        accepted_study_types = {'Recruiting', 'Enrolling by invitation', 'Active, not recruiting'}
        Dict = fill_dict(data, Dict, years_ago, accepted_study_types)
        #New
        years_ago = datetime.now() - timedelta(days = 2 * 365) #two years
        accepted_study_types = {'Not yet recruiting', 'Recruiting', 'Enrolling by invitation', 'Active, not recruiting', 'Suspended', 'Completed'}
        Dict = fill_dict(data, Dict, years_ago, accepted_study_types)
        conversion(Dict, outputFile)


def main():
    if len(sys.argv) < 2:
        print('Usage: python Filter.py <file1>')
        return

    filename1 = sys.argv[1]
    filter(filename1)

     
if __name__ == '__main__':
    main()
