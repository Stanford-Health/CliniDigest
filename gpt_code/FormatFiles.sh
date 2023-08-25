#!/bin/bash

# fill in sbatch info

module purge

# TODO: add full path before all folders
# ex: rm -r /labs/mpsnyder/arjo/gpt_code/internal_files/devices_gpt_input
rm -r gpt_code/internal_files/devices_gpt_input
mkdir gpt_code/internal_files/devices_gpt_input

rm -r gpt_code/internal_files/devices_references
mkdir gpt_code/internal_files/devices_references

# TODO: add full path before all folders
# ex: srun python /labs/mpsnyder/arjo/gpt_code/FormatFiles.py DevicesCombos.json
srun python gpt_code/FormatFiles.py DevicesCombos.json
