import csv
import json
import numpy as np
import regex as re
import sys
from collections import defaultdict
from util import *
from Classify import *


def find_diff(oldFile, newFile):
    trials_to_classify = {}
    trials_to_remove = {}

    with open('' + oldFile, encoding = 'utf8') as FILE1:
        with open('' + newFile, encoding = 'utf8') as FILE2:
            old_data = json.load(FILE1)
            new_data = json.load(FILE2)
            key_list = new_data.keys()

            for key in key_list:
                old_set = set(tuple(item for item in cur_list) for cur_list in old_data[key][1:] if len(old_data[key]) > 1)
                new_set = set(tuple(item for item in cur_list) for cur_list in new_data[key][1:] if len(new_data[key]) > 1)
                added = new_set - old_set
                removed = old_set - new_set
                if len(added) != 0:
                    trials_to_classify[key] = list(added)
                if len(removed) != 0:
                    trials_to_remove[key] = list(removed)
    return trials_to_classify, trials_to_remove


def format_new_files(file, Dict):
    if len(Dict) != 0:
        with open(file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            headers = ['Link', 'Title', 'Description', 'Primary Category', 'Secondary Category', 'Tertiary Category']
            writer.writerow(headers)
            for trials in Dict.values():
                writer.writerows(trials)


def delete_old_files(master_folder, Dict):
    combos_to_rerun = defaultdict(list)
    for device, trials in Dict.items():
        data = {}
        with open(f'devices_{master_folder + device}.json') as master:
            data = json.load(master)
            for trial in trials:
                for field, existing_trials in data.items():
                    if list(trial) in existing_trials:
                        data[field][0] -= 1
                        data[field].remove(list(trial))
                        if field not in combos_to_rerun[device]:
                            combos_to_rerun[device].append(field)
            conversion(data, f'devices_{master_folder + device}.json')
    return combos_to_rerun


def add_new_files(master_folder, Dict, combos_to_rerun):
    predictions = get_file_contents('internal_files/predictions_devices_gpt.txt').split('\n')
    index = 0
    for device, trials in Dict.items():
        with open(f'devices_{master_folder + device}.json') as master:
            data = json.load(master)
            for trial in trials:
                medical_field = ''.join(predictions[index].title().split())
                if medical_field == '':
                    medical_field = 'Other'
                #print(trial)
                if list(trial) not in data[medical_field]:
                    data[medical_field][0] += 1
                    data[medical_field].append(trial)
                    if medical_field not in combos_to_rerun[device]:
                        combos_to_rerun[device].append(medical_field)
                index += 1
            conversion(data, f'devices_{master_folder + device}.json')
    return combos_to_rerun


def main():
    if len(sys.argv) < 3:
        print("Usage: python FindDiff.py <file1> <file2>")
        return

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    csv_filename = f'internal_files/DevicesTrialsToAdd.csv'

    #find difference
    trials_to_classify, trials_to_remove = find_diff(filename1, filename2)

    #delete old files
    combos_to_rerun = delete_old_files('master_lists/', trials_to_remove)

    #format new files
    format_new_files(csv_filename, trials_to_classify)

    #predict labels
    predict(csv_filename)

    #add new files
    combos_to_rerun = add_new_files('master_lists/', trials_to_classify, combos_to_rerun)

    conversion(combos_to_rerun, f'internal_files/DevicesCombos.json')


if __name__ == '__main__':
    main()

