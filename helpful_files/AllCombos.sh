#!/bin/bash

#SBATCH --job-name=combos
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=batch
#SBATCH --time=0-1:00:00
#SBATCH --output=output/Download.out
#SBATCH --error=error/Download.err
#SBATCH --mail-user=FILL_IN
#SBATCH --account=FILL_IN

module purge

. venv/bin/activate
srun python helpful_files/AllCombos.py
