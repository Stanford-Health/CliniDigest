import json
import os
import configparser


def conversion(Dict, json_name):
    json_object = json.dumps(Dict, indent=4)
    with open(json_name, 'w', encoding = 'utf-8') as outfile:
        outfile.write(json_object)

def get_file_contents(FileName):
    with open(FileName, 'r', encoding='utf-8') as file:
        data = file.read()
        return data

def read_config():
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(r'internal_files/config.ini')
    return config
