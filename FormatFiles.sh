#!/bin/bash

#SBATCH --job-name=format
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=batch
#SBATCH --time=0-1:00:00
#SBATCH --output=output/Format.out
#SBATCH --error=error/Format.err
#SBATCH --account=FILL_IN
#SBATCH --mail-user=FILL_IN
#SBATCH --mail-type=END,FAIL

module purge

rm -r internal_files/devices_gpt_input
mkdir internal_files/devices_gpt_input

rm -r internal_files/devices_references
mkdir internal_files/devices_references

. venv/bin/activate
srun python FormatFiles.py DevicesCombos.json
