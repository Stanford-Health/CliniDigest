import json

# TODO: replace dir with your full path
dir = f'/labs/mpsnyder/arjo/'

def conversion(Dict, json_name):
    json_object = json.dumps(Dict, indent=4)
    with open(json_name, 'w', encoding = 'utf-8') as outfile:
        outfile.write(json_object)

def get_file_contents(FileName):
    with open(FileName, 'r', encoding='utf-8') as file:
        data = file.read()
        return data
