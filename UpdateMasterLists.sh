#!/bin/bash

#SBATCH --job-name=update
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=batch
#SBATCH --account=mpsnyder
#SBATCH --time=0-1:00:00
#SBATCH --output=output/Update.out
#SBATCH --error=error/Update.err
#SBATCH --mail-user=FILL_IN
#SBATCH --mail-type=END,FAIL

module purge

# Do work!
. venv/bin/activate
srun python UpdateMasterLists.py internal_files/PastDevices.json internal_files/Devices.json