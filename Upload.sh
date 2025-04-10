#!/bin/bash

#SBATCH --job-name=uploading
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=batch
#SBATCH --time=1-0:00:00
#SBATCH --output=output/Upload.out
#SBATCH --error=error/Upload.err
#SBATCH --account=FILL_IN
#SBATCH --mail-user=FILL_IN
#SBATCH --mail-type=END,FAIL


current_date=$(date +%F)

date_folder="$current_date"
references_folder="$date_folder/references"
summaries_folder="$date_folder/summaries"

mkdir "$date_folder"
mkdir "$references_folder"
mkdir "$summaries_folder"

cp -r internal_files/devices_gpt_output/* "$summaries_folder"
cp -r internal_files/devices_references/* "$references_folder"

cp -r internal_files/devices_gpt_output/* current_outputs/summaries
cp -r internal_files/devices_references/* current_outputs/references

find current_outputs/references -type f -empty -delete
find current_outputs/summaries -type f -empty -delete