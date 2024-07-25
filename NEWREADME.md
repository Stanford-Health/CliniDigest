# CliniDigest Pipeline README

This repository contains a detailed automated pipeline for processing and analyzing clinical trials data. The pipeline consists of multiple interdependent scripts that are executed in sequence to perform various tasks.

## Pipeline Overview

Overview
This project automates a series of tasks using SLURM job scheduler scripts. The Everything.sh script coordinates the execution of several dependent jobs, ensuring that each step is completed successfully before moving on to the next.

Scripts
This is the main script that orchestrates the execution of several dependent jobs in a sequential manner. The jobs include downloading data, updating master lists, formatting files, running GPT scripts, creating website files, and uploading results. The script uses SLURM job dependencies to ensure proper execution order.

Job Details
Download Job

Script: Download.sh
Job Name: Download
Output: DandF.out
Error: DandF.err
Update Master Lists Job

Script: UpdateMasterLists.sh
Job Name: Update
Output: UpdateMaster.out
Error: UpdateMaster.err
Dependency: After Download job
Format Files Job

Script: FormatFiles.sh
Job Name: Format
Output: Format.out
Error: Format.err
Dependency: After Update job
GPT Job

Script: Gpt.sh
Job Name: Gpt
Output: Gpt.out
Error: Gpt.err
Dependency: After Format job
Website File Creation Job

Script: Upload.sh
Job Name: Upload
Output: Upload.out
Error: Upload.err
Dependency: After Gpt job
Usage
To run the entire workflow, execute the Everything.sh script using the following command: sbatch Everything.sh
This will submit the Everything.sh script to the SLURM job scheduler, which will then manage the execution of all the dependent jobs in the correct order.

Other Scripts
Download.py
The Download.py script is designed to search for and download clinical trial data from the ClinicalTrials.gov API. It processes the data to identify and track devices mentioned in the trials, based on predefined search terms.

UpdateMasterLists.py
The UpdateMasterLists.py script compares the past and current device lists, updates the master lists, and categorizes new trials based on predictions.

FormatFiles.py
The FormatFiles.py script processes the device and medical field combinations that need to be re-run, formats the data, and generates input files for GPT processing. The script splits the data into manageable chunks based on token count limits.

Gpt.py
The Gpt.py script processes the formatted trial data, generates prompts, and uses OpenAI's GPT-4 model to create summaries and theses about the purpose of various devices in medical fields.

Upload.sh
The Upload.sh script is responsible for organizing and uploading the output files to the appropriate directories. It creates date-specific folders for today's date, copies generated summary and reference files to these folders, and also backs up the files to a website backup directory. Finally, it removes any empty files from the backup directories.

*Folders*
- **devices_master_lists:** Contains JSON files with master lists of devices related to various medical fields. These JSON files include information about devices categorized by medical fields, providing details such as clinical trial links, titles, and descriptions.
    Within the devices master lists folder, the following JSON files are included:
        - Actigraph_CentrePoint_Insight.json
        - Apple_Watch_5.json
        - Biostrap_Evo.json
        - Coros_Pace.json
        - Cronometer.json
        - Dexcom_G6_Pro.json
        - Dreem_Headband_3.json
        - Fitbit_Charge_4.json
        - Fitbit_Sense.json
        - Garmin_Fenix_7S.json
        - Google_Fit.json
        - MyFitnessPal.json
        - Nutrisense_CGM.json
        - Oura_Ring_Gen_3.json
        - Polar_H10.json
        - Polar_Vantage_V2.json
        - Polar_Verity_Sense.json
        - SleepOn_Go2Sleep.json
        - Strava.json
        - Suuntu_9_Peak_Pro.json
        - Suuntu_HR_Belt.json
        - Whoop_Strap_4.0.json
        - Withings_Body+.json
        - Withings_ScanWatch.json
        - Withings_Sleep.json
    
    - **internal_files:** Includes internal files for data manipulation and processing. The following files will be created:
        - **Devices.json:** JSON file containing device information for data processing.
        - **DevicesCombos.json:** JSON file with combinations of devices used in the pipeline.
        - **DevicesTrialsToAdd.csv:** CSV file listing additional trials to be added for specific devices.
        - **Manufacturers.json:** JSON file containing manufacturer information for data processing.
        - **ManufacturersTrialsToAdd.csv:** CSV file listing additional trials to be added for specific manufacturers.
        - **PastDevices.json:** JSON file containing historical device information.
        - **PastManufacturers.json:** JSON file containing historical manufacturer information.
        These files are used internally for various tasks related to data manipulation, processing, and addition of new trials to existing device and manufacturer information.

Configuration File: internal_files/config.ini
The config.ini file contains various settings and parameters used by the scripts in this project. Below are the sections and their respective keys:

[Devices]
devices: List of devices to track, separated by commas.
[AlgSearchTerms]
Search Terms: Mappings of search terms to device names. The key is the search term (can include underscores) and the value is the corresponding device name.
[FormattedAlgSearchTerms]
Formatted Search Terms: Similar to [AlgSearchTerms] but with search terms grouped by device.
[MedicalFields]
file_fields: List of medical fields used in file-based operations.
text_fields: List of medical fields used in text-based operations.
[OpenAIAPI]
key: API key for accessing OpenAI services.
model: OpenAI model to be used (e.g., gpt-4-0125-preview).

Required Packages
numpy - For numerical operations.
regex - For regular expression operations.
json - For handling JSON files (comes with Python standard library, no need to install separately).
openai - For interacting with OpenAI's GPT models.
tiktoken - For tokenization with OpenAI models.
scipy - For scientific and technical computing.
matplotlib - For plotting and visualization (if you need plotting in the future).

## Getting Started

To start the automated pipeline, follow these steps:

1. Fill in the necessary SLURM job details in each script (MainCode.sh, WebsiteCode.sh, etc.).

2. Replace the placeholders (ex: /labs/mpsnyder/arjo/clinical_trials_code/MainCode.sh) with the full paths to the respective script files.

3. Submit 'MasterScript.sh', which will take care of dependencies as outlined in the script.