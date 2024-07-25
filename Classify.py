import csv
import openai
import regex as re
import sys
import time

from util import read_config

max_retries = 5
retry_delay = 5  # seconds

def read_csv_to_dict(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        columns = {header: [] for header in headers}

        for row in reader:
            for header, value in zip(headers, row):
                columns[header].append(value)

    return columns


def get_completion(prompt, model):
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def predict(csv_file_path):
    config = read_config()
    clinical_trials = read_csv_to_dict(csv_file_path)
    clinical_trial_title = clinical_trials["Title"]
    clinical_trial_descriptions = clinical_trials["Description"]

    full_results = []
    medical_fields = config.get('MedicalFields', 'text_fields').split(', ')
    openai.api_key = config.get('OpenAIAPI', 'key')
    openai_model = config.get('OpenAIAPI', 'model')
    num_fields = len(medical_fields)
    field_list = "\n".join([f"- {field}" for field in medical_fields])

    for i in range(len(clinical_trial_descriptions)):
        prompt = f'''You are provided with a set of {num_fields} medical field classes: {", ".join(f'"{field}"' for field in medical_fields)}. 
Your task is to analyze the given clinical trial title and description and classify it into one of these {num_fields} medical field classes. Please provide only one field as your output.
---
Trial Title: {clinical_trial_title[i]}
Trial Description: {clinical_trial_descriptions[i]}
---
Task: Classify the clinical trial into one of the {num_fields} specified medical field classes:
{field_list}
Please provide only the medical field name as your output.
'''        
        response = ''
        for retry in range(max_retries):
            try:
                response = get_completion([{"role": "user", "content": prompt}], openai_model)
                time.sleep(1)
                break  

            except Exception as e:
                print(f"Error: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        else:
            print("Max retries reached. Could not complete the action.")

        response = get_completion([{"role": "user", "content": prompt}], openai_model)
        if response == 'Hematology':
            response = 'Oncology'
        for field in medical_fields:
            if field in response:
                response = field
                break
        else:
            response = 'Other'
        full_results.append(response)
    name = re.match('.*\/(.*)TrialsToAdd.csv', csv_file_path).group(1)
    with open(f'internal_files/predictions_{name.lower()}_gpt.txt', 'w') as output:
        output.writelines('\n'.join(full_results))
