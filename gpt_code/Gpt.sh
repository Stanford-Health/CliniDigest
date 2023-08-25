#!/bin/bash

# fill in sbatch info

module purge

# TODO: add full path before all folders
# ex: rm -r /labs/mpsnyder/arjo/gpt_code/internal_files/devices_gpt_output
rm -r gpt_code/internal_files/devices_gpt_output
mkdir gpt_code/internal_files/devices_gpt_output

# TODO: add full path before code, not json file
# ex: srun python /labs/mpsnyder/arjo/gpt_code/Gpt.py internal_files/devices_gpt_input
srun python gpt_code/Gpt.py internal_files/devices_gpt_input
