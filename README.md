# CliniDigest Pipeline README

This repository contains a detailed automated pipeline for processing and analyzing clinical trials data. The pipeline consists of multiple interdependent scripts that are executed in sequence to perform various tasks.

## Pipeline Overview

The pipeline is designed to automate the processing of clinical trials data. It involves several steps, each performed by a specific script. The scripts are executed in a sequence that maintains dependencies between them.

1. **DownloadCode.sh:** This script initiates the pipeline by submitting the download job, which is responsible for downloading and preparing the clinical trials data.

2. **DownloadCode.py:** The download job extracts essential information from the downloaded data. It serves as the starting point of the pipeline.

   - **Description:** This Python script processes the downloaded clinical trials data. It uses the BeautifulSoup library to parse XML data from the clinical trial files. The script extracts various fields from the XML data, such as agency, condition, description, intervention, and more. It then performs searches based on specific device and manufacturer terms using predefined dictionaries. The matched data is stored in separate dictionaries for devices and manufacturers.
   - **Dependencies:** The script depends on the BeautifulSoup library for XML parsing. The script also depends on the `util` module for the `conversion` function, which is used to save filtered data as JSON files.
   - **Execution:** The script is executed as part of the pipeline and plays a crucial role in processing and filtering clinical trials data.

3. **WebsiteCode.sh:** This script submits the website job after the main job successfully completes. The website job may generate web-related content based on the processed data.

4. **WebsiteCode.py:** The website job script filters data from the MainDevices.json and MainManufacturers.json files and prepares it for web-related content generation.

   - **Description:** This Python script filters data extracted from clinical trials and prepares it for generating web content. It loads the data from MainDevices.json and MainManufacturers.json files, processes it by removing the last entry from each device's data, and saves the filtered data into WebsiteDevices.json and WebsiteManufacturers.json files. 
   - **Dependencies:** The script depends on the `util` module for the `conversion` function, which is used to save filtered data as JSON files.
   - **Execution:** The script is executed as part of the pipeline after the MainCode.py script and before the subsequent steps. It prepares the data for web-related content generation.

5. **Filter.sh:** The filter job is submitted after the download job. It processes the data further applying filters.

6. **Filter.py:** The filter script processes and filters the clinical trials data based on various criteria.

   - **Description:** This Python script reads data from MainDevices.json and MainManufacturers.json files, applies filters to the data based on criteria such as study type, enrollment, and end date, and creates filtered output files in the internal_files folder.
   - **Dependencies:** The script depends on the `util` module for the `conversion` function and other utilities. It also uses the datetime module for date calculations.
   - **Execution:** The script is executed as part of the pipeline to filter and process clinical trials data.

7. **UpdateMasterLists.sh:** This script updates master lists based on filtered data. It is executed after the filter job.

8. **UpdateMasterLists.py:** The update master lists script compares two JSON files, identifies differences in data between them, formats new files, predicts labels, and adds new files to master lists.

   - **Description:** This Python script reads two JSON files, compares their contents, identifies differences (trials to classify and trials to remove), formats new files for trials to classify, removes old trials, predicts labels using a classifier (GPT-based), and updates master lists accordingly.
   
   ### Predict.py Script (Medical Field Classification)

   The `predict.py` script is a part of the Medical Field Classifier used within the `UpdateMasterLists.py` script. This script leverages the OpenAI GPT-3.5 model to classify clinical trial descriptions into specific medical field categories. The classification process involves generating predictions based on the given clinical trial descriptions and mapping them to predefined medical field classes.

   #### Dependencies

   - OpenAI Python Client: The script uses the OpenAI Python client to interact with the GPT-3.5 model.
   - `process_data.py`: The script relies on the `process_data.py` module for reading and processing CSV data containing clinical trial descriptions.

   #### Usage

   The `predict.py` script is executed within the `UpdateMasterLists.py` script to predict medical field categories for clinical trial descriptions. Here's how it works:
   
   #### Note

   - The `predict.py` script requires an OpenAI API key, which must be filled in the `openai.api_key` field within the script.
   - The script handles potential API errors with retries to ensure robustness.
   - The predicted medical field classes are mapped to specific categories based on predefined medical fields and keywords.

   For more information on the Medical Field Classifier and the underlying GPT-3.5 model, refer to the [OpenAI API documentation](https://beta.openai.com/docs/api-reference/introduction).
   
   - **Dependencies:** The script depends on the `util` module for the `conversion` function. It also uses the `regex`, `collections`, and `predict` modules for various tasks.
   - **Execution:** The script is executed as part of the pipeline to update master lists based on filtered data.

9. **FormatFiles.sh:** The format job is dependent on the update job. It performs additional formatting on the processed data.

10. **FormatFiles.py:** The script further processes and formats the data for input to the GPT model.

   - **Description:** The script is responsible for processing the clinical trials data and formatting it for input to the GPT model. This is necessary to ensure that the data is correctly structured and tokenized before being passed to the GPT model for further analysis.
   - **Dependencies:** The script depends on various utility functions from the `util` module for tasks such as data conversion and file manipulation. The script uses the `tiktoken` library to calculate the number of tokens in a text string.
   - **Execution:** The script performs the following steps:
      1. Reads data from JSON files containing medical field information.
      2. Processes and formats the data to create input files for the GPT model.
      3. Determines the number of tokens in each formatted input and creates multiple files if necessary to avoid token limits.
      4. Generates reference lists for each medical field to track the corresponding clinical trials.

11. **Gpt.sh:** The GPT job executes after the format job. It involves using the GPT model to generate content.

12. **Gpt.py:** The script is a critical component of the automated pipeline, responsible for generating content based on summaries and clinical trials. 

   - **Description:** The script utilizes the OpenAI GPT-3.5 model to generate content in response to prompts using the GPT-3.5 model, constructing prompts based on clinical trials, device names, and medical fields.
   - **Dependencies:** The script imports necessary libraries and modules such as `datetime`, `openai`, `os`, `random`, `regex`, and `util`.
   - **OpenAI API Key:** Provide your OpenAI API key in the `openai.api_key` field before using the script.
   - **Execution:** The script is executed as part of the pipeline to create summaries.

13. **Upload.sh:** The upload job is submitted after the GPT job and handles uploading the processed and generated data to a destination.

   - **Description:** This shell script organizes and uploads the generated content and references from the GPT process. It creates a folder structure based on the current date and copies the generated content to appropriate backup directories.
   - **Execution:** Run the script to initiate the upload process. Ensure the correct paths are configured for copying the generated content and references.

## Necessary Files

1. **clinical_code folder**
    The `clinical_code` directory contains scripts and folders related to the clinical trials download and other pipeline tasks.

    Within the clinical trials folder, the following files are included:
    - **DownloadCode.py:** The Python script responsible for processing downloaded clinical trials data.
    - **DownloadCode.sh:** The shell script that initiates the download job and executes DownloadCode.py.
    - **util.py:** A utility module providing functions for data conversion and manipulation.
    - **WebsiteCode.py:** The Python script responsible for generating web-related content based on filtered data.
    - **WebsiteCode.sh:** The shell script that submits the website job and executes WebsiteCode.py.

    Within the clinical trials folder, the following files will be created:
    - **MainDevices.json:** A JSON file containing extracted data related to medical devices.
    - **MainManufacturers.json:** A JSON file containing extracted data related to medical device manufacturers.
    - **MainDevices.json:** A JSON file containing extracted data related to medical devices.
    - **MainManufacturers.json:** A JSON file containing extracted data related to medical device manufacturers.

2. **gpt_code folder**
    The `gpt_code` directory contains scripts and folders related to the GPT-based content generation and other pipeline tasks.

    Within the gpt code folder, the following files are included:
    - **Filter.sh:** The filter job is submitted after the main job. It processes the data further, possibly applying filters or transformations.
    - **Filter.py:** The filter script processes and filters the clinical trials data based on various criteria.
    - **FormatFiles.sh:** The `FormatFiles.sh` shell script performs various cleanup and execution tasks related to the `FormatFiles.py` script.
    - **Gpt.sh:** The GPT job executes after the format job. It involves using the GPT model to generate content.
    - **Gpt.py:** The `Gpt.py` script is a critical component of the automated pipeline, responsible for generating content based on summaries and clinical trials.
    - **MasterScript.sh:** A script that potentially coordinates and runs various pipeline components.
    - **UpdateMasterLists.py:** The update master lists script compares two JSON files, identifies differences in data between them, and updates master lists.
    - **UpdateMasterLists.sh:** The shell script that submits the update master lists job and executes UpdateMasterLists.py.
    - **Upload.sh:** The upload job is submitted after the GPT job and handles uploading the processed and generated data to a destination.
    - **util.py:** A utility module providing functions for data conversion and manipulation.

    Within the gpt code folder, the following folders are included:
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
    
    - **manufacturers_master_lists:** Contains JSON files with master lists of manufacturers related to various medical fields. These JSON files include information about devices categorized by medical fields, providing details such as clinical trial links, titles, and descriptions.
    Within the manufacturers master lists folder, the following JSON files are included:
        - Actigraph.json
        - Apple.json
        - Biostrap.json
        - Coros.json
        - Cronometer.json
        - Dexcom.json
        - Dreem.json
        - Fitbit.json
        - Garmin.json
        - Google.json
        - MyFitnessPal.json
        - Nutrisense.json
        - Oura.json
        - Polar.json
        - SleepOn.json
        - Strava.json
        - Suuntu.json
        - Withings.json
        - Whoop.json
    
    - **MedicalFieldClassifier-main:** Submodule or directory related to the Medical Field Classifier. It contains the following files:
        - **LICENSE:** The license file for the Medical Field Classifier.
        - **GPTClassifier:** Within the GPTClassifier folder, the following files are included:
            - **evaluation.py:** Python script for evaluating the performance of the classifier.
            - **main.py:** Main Python script for running the classifier and making predictions.
            - **predict.py:** Python script for making predictions using the trained classifier.
            - **process_data.py:** Python script for processing data before classification.
            Within the GPTClassifier folder, the following files will be created:
            - **predictions_devices_gpt.txt:** Text file containing predictions for devices using GPT.
 

## Getting Started

To start the automated pipeline, follow these steps:

1. Fill in the necessary SLURM job details in each script (MainCode.sh, WebsiteCode.sh, etc.).

2. Replace the placeholders (ex: /labs/mpsnyder/arjo/clinical_trials_code/MainCode.sh) with the full paths to the respective script files.

3. Submit 'MasterScript.sh', which will take care of dependencies as outlined in the script.

## Dependencies

- SLURM: The pipeline uses SLURM job scheduler to manage job submission and dependencies.
- Python: The pipeline includes Python scripts (MainCode.py, WebsiteCode.py) for data processing and filtering.
- Dependencies: Any dependencies specific to each script should be documented within the script itself.

## Note

Please be cautious when running the pipeline, ensuring that the required permissions and resources are available.

For any questions or assistance, contact [reneedw@cs.stanford.edu](mailto:your_email@example.com).
