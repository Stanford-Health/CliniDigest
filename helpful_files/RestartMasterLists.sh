#!/bin/bash

#SBATCH --job-name=restart
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=batch
#SBATCH --account=mpsnyder
#SBATCH --time=0-1:00:00
#SBATCH --output=/labs/mpsnyder/arjo/gpt_code/output/%j.out
#SBATCH --error=/labs/mpsnyder/arjo/gpt_code/error/%j.err

for f in /labs/mpsnyder/arjo/gpt_code/devices_master_lists/*; do 
    cp /labs/mpsnyder/arjo/gpt_code/helpful_files/Template.json "$f"
done
for f in /labs/mpsnyder/arjo/gpt_code/temp_manufacturers_master_lists/*; do 
    cp /labs/mpsnyder/arjo/gpt_code/helpful_files/Template.json "$f"
done
