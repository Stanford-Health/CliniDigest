# CliniDigest Pipeline README

This repository contains a detailed automated pipeline for processing and analyzing clinical trial data. The pipeline consists of multiple interdependent scripts that are executed in sequence to perform various tasks.

## Getting Started

To start the automated pipeline, follow these steps:

1. Fill in the necessary SLURM job details in each script (MainCode.sh, WebsiteCode.sh, etc.).

2. Replace the placeholders with the full paths to the respective script files.

3. Run sbatch 'Everything.sh' to run the pipeline, which will take care of dependencies as outlined in the script.

## Dependencies

- SLURM: The pipeline uses SLURM job scheduler to manage job submission and dependencies.
- Python: The pipeline includes Python scripts (MainCode.py, WebsiteCode.py) for data processing and filtering.
- Dependencies: Any dependencies specific to each script should be documented within the script itself.

# 🛠 Clinical Trial Summarization Pipeline Management

This Python script manages the configuration and metadata used in a clinical trial summarization pipeline. It allows users to modify:

- Medical text/file fields
- Devices
- Search terms used for detecting devices in raw clinical trial text

---

## 📦 Features

- View current pipeline values
- Add, change, or delete:
  - Medical fields
  - Devices (and corresponding search terms)
  - Search terms associated with each device
- Automatically updates and rewrites the configuration file
- Updates master JSON lists per device
- Rebuilds historical `PastDevices.json` records

---

## 📂 Config File (`config.ini`) Structure

```ini
[MedicalFields]
text_fields = summary, intervention, detailed_description
file_fields = nct_id

[Devices]
devices = Apple_HealthKit, Garmin_Watch, Fitbit

[AlgSearchTerms]
garmin = Garmin_Fenix
google[ -]?fit = Google_Fit

[FormattedAlgSearchTerms]
Garmin_Fenix = garmin
Google_Fit = google[ -]?fit
```

# 🧠 What Can You Do?

## 1. 📋 View Current Values

Displays:

- Medical fields  
- Tracked devices  
- Search term mappings  

---

## 2. 🛠 Modify Pipeline Values

You'll be prompted to choose:

- Medical Fields  
- Devices  
- Search Terms  

---

## ➕ Adding a New Device

1. Choose **Devices** from the "Change pipeline values" menu.  
2. Select **Add**.  
3. Input the new device name (e.g., `Google_Pixel_Watch`).  
4. Enter associated search terms (e.g., `pixel watch`, `google smartwatch`).
   - See [How to Create Search Terms](newsearchterms) for more information
   - Use `_` for leading/trailing spaces (e.g., `_fitbit` = `" fitbit"`).  
6. Type `0` to finish adding terms.  
7. Confirm your entries.  

### ✅ The Script Will:

- Add the device to `config.ini`
- Add search terms to `AlgSearchTerms` and `FormattedAlgSearchTerms`
- Alphabetize entries
- Create a new `devices_master_lists/<device>.json` from `Template.json`
- Update `Devices.json` and `PastDevices.json`

---

## ✏️ Changing a Device Name

1. Choose **Devices → Change**  
2. Select the device to rename  
3. Enter the new name  

### The Script Updates:

- `Devices`, `Formatted Search Terms`, and `AlgSearchTerms`
- Master list filenames
- JSON content references

---

## ❌ Deleting a Device

1. Choose **Devices → Delete**  
2. Select the device  

### The Script Will:

- Remove the device from all config sections
- Update `Devices.json` and `PastDevices.json`
- Delete the corresponding `.json` from `devices_master_lists/`

---

## 🧷 Modifying Search Terms

Choose **Search Terms** from the main menu.

### ➕ Add Terms

- Choose a device  
- Input new search terms  
- Script updates the mappings and config file

### ✏️ Change All Terms

- Replaces **all current search terms** for a device  
- Old terms are removed from the config

### ❌ Delete a Specific Term

- Choose the device  
- Select the search term to delete  
- **Note**: Deletion is blocked if it's the only remaining term

---
## How to Create New Search Terms
1. Go to [clinicaltrials.gov](https://clinicaltrials.gov/) and type in potential device names in the Other Terms field.
2. Try several terms similar to the device you have. Typos are common in clinical trial documentation.
3. For example, for the MyFitnessPal device, the following search terms are needed to capture them all: myfitnesspal, myfitness pal, my fitnesspal, my fitness pal
   - This process will involve hand-checking whether the search terms are too broad or too narrow.
   - In some cases, such as the Apple HealthKit, the search term healthkit was not sufficiently narrow, so a regular expression was produced to search for other relevant terms in addition to health kit, such as iPhone, Apple, and/or iOS.
   - You may also find the regular expressions defined in the config.ini file for each existing device helpful when ideating on new devices.
   - Notes:
      - During the search process, all text is converted to lower-case, so all search terms will also be lower-case.
      - It is also not necessary to create regular expressions for new search terms. Inputting each search term individually will have the same effect as the creation of a regular expression connecting each with an or. Regular expressions are useful for multi-word device names or devices that require more complex searches.
   - Please reach out if you need help identifying sufficient search terms.
4. Iterate through several search terms until you feel sufficiently confident in your search terms.
5. Add them to the pipeline using one of the methods above, depending on the context in which you are adding the search terms. 
---

## 📁 Reset Master Lists

To reinitialize all downstream files from the updated config, run:

```bash
sbatch helpful_files/RestartMasterLists.sh
```

## 🧠 Tips

- Always use **Title_Case** for device names.  
- Use `_` to signify spaces in search terms (e.g., `_fitbit` → `" fitbit"`).  
- Be cautious with deletions: downstream summaries may be affected.

---

## 🔐 OpenAI API

Ensure your `config.ini` contains the following:

```ini
[OpenAIAPI]
key = your-api-key-here
model = gpt-4-0125-preview
```

## Note

Please be cautious when running the pipeline, ensuring that the required permissions and resources are available.

For any questions or assistance, contact [reneedw@cs.stanford.edu](mailto:your_email@example.com).
