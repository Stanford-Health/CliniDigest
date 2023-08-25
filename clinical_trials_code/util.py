import json
import os

#TODO: add full path before folder name
input_output_folder = 'clinical_trials_code/'

def conversion(Dict, json_name):
    json_object = json.dumps(Dict, indent=4)
    with open(json_name, 'w', encoding = 'utf-8') as outfile:
        outfile.write(json_object)
