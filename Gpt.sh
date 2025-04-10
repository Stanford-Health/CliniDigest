#!/bin/bash

#SBATCH --job-name=gpt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=batch
#SBATCH --time=0-1:00:00
#SBATCH --output=output/Gpt.out
#SBATCH --error=error/Gpt.err
#SBATCH --account=FILL_IN
#SBATCH --mail-user=FILL_IN
#SBATCH --mail-type=END,FAIL

module purge

rm -r internal_files/devices_gpt_output
mkdir internal_files/devices_gpt_output

# Do work!
. venv/bin/activate
srun python Gpt.py internal_files/devices_gpt_input
