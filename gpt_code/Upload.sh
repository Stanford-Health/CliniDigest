#!/bin/bash

# fill in sbatch info


current_date=$(date +%F)

date_folder="/labs/mpsnyder/arjo/gpt_code/$current_date"
references_folder="$date_folder/references"
summaries_folder="$date_folder/summaries"

mkdir "$date_folder"
mkdir "$references_folder"
mkdir "$summaries_folder"

cp -r /labs/mpsnyder/arjo/gpt_code/internal_files/devices_gpt_output/* "$summaries_folder"
cp -r /labs/mpsnyder/arjo/gpt_code/internal_files/devices_references/* "$references_folder"

cp -r /labs/mpsnyder/arjo/gpt_code/internal_files/devices_gpt_output/* /labs/mpsnyder/arjo/gpt_code/website_backup/summaries
cp -r /labs/mpsnyder/arjo/gpt_code/internal_files/devices_references/* /labs/mpsnyder/arjo/gpt_code/website_backup/references

