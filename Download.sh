#!/bin/bash

#SBATCH --job-name=d_and_f
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=128000
#SBATCH --cpus-per-task=1
#SBATCH --partition=batch
#SBATCH --account=mpsnyder
#SBATCH --time=1-0:00:00
#SBATCH --output=output/Download.out
#SBATCH --error=error/Download.err
#SBATCH --mail-user=FILL_IN
#SBATCH --mail-type=END,FAIL

module purge

. venv/bin/activate

mv internal_files/Devices.json internal_files/PastDevices.json

srun python Download.py
