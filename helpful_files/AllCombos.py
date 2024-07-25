import json
import os
import sys

sys.path.append('/labs/mpsnyder/arjo/gpt_code')

from util import *

input_folder = r'/labs/mpsnyder/arjo/gpt_code/devices_master_lists'

result = {}

for filename in sorted(os.listdir(input_folder)):
    with open(os.path.join(input_folder, filename), "r") as file:
        data = json.load(file)
        device_name = filename[:-5]

        medical_fields = []
        for field, content in data.items():
            if len(content) > 1:
                medical_fields.append(field)

        if medical_fields:
            result[device_name] = medical_fields

conversion(result, 'internal_files/DevicesCombos.json')
