#!/bin/bash

# fill in sbatch info

module purge

# TODO: add full path before all folders
# ex: rm -r /labs/mpsnyder/arjo/gpt_code/internal_files/combos_to_rerun
rm -r gpt_code/internal_files/combos_to_rerun
mkdir gpt_code/internal_files/combos_to_rerun

# TODO: add full path before all folders
# ex: srun python /labs/mpsnyder/arjo/gpt_code/UpdateMasterLists.py internal_files/PastDevices.json internal_files/Devices.json
srun python gpt_code/UpdateMasterLists.py internal_files/PastDevices.json internal_files/Devices.json
srun python gpt_code/UpdateMasterLists.py internal_files/PastManufacturers.json internal_files/Manufacturers.json
