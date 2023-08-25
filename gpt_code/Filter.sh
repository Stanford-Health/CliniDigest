#!/bin/bash

# fill in sbatch info

module purge

# TODO: add full path before each filename
# ex:
# mv /labs/mpsnyder/arjo/gpt_code/internal_files/Devices.json /labs/mpsnyder/arjo/gpt_code/internal_files/PastDevices.json
mv gpt_code/internal_files/Devices.json gpt_code/internal_files/PastDevices.json
mv gpt_code/internal_files/Manufacturers.json gpt_code/internal_files/PastManufacturers.json

# TODO: add full path before code, not json file
# ex: srun python /labs/mpsnyder/arjo/gpt_code/Filter.py MainDevices.json
srun python gpt_code/Filter.py MainDevices.json
srun python gpt_code/Filter.py MainManufacturers.json

