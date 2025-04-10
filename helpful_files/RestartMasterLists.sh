#!/bin/bash

#SBATCH --job-name=restart
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=batch
#SBATCH --account=FILL_IN
#SBATCH --time=0-1:00:00
#SBATCH --output=output/Download.out
#SBATCH --error=error/Download.err
#SBATCH --mail-user=FILL_IN

for f in /labs/mpsnyder/arjo/gpt_code/devices_master_lists/*; do 
    cp /labs/mpsnyder/arjo/gpt_code/helpful_files/Template.json "$f"
done