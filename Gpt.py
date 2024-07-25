import datetime
import openai
import os
import random
import regex as re
import sys
import time
from util import *


def get_completion(prompt, model="gpt-4-0125-preview"):
    max_retries = 10
    retry_delay = 5  # seconds
    messages = [{'role': 'user', 'content': prompt}]
    for retry in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0, # this is the degree of randomness of the model's output
            )
            return response.choices[0].message['content']

        except Exception as e:
            print(f"Error: {e}")
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    raise Exception(f"Max retries reached. Could not complete the action. Prompt = {prompt}")


def get_prompt_variables(device_name, medical_field):
    prompt_device_name = ' '.join(device_name.split('_'))
    if device_name not in ['Cronometer', 'Google_Fit', 'MyFitnessPal', 'Strava']:
        if device_name[0] in 'AO':
            prompt_device_name = 'an ' + prompt_device_name
        else:
            prompt_device_name = 'a ' + prompt_device_name

            prompt_medical_field = medical_field.lower()

    prompt_medical_field = medical_field.lower()
    if medical_field == 'Chronic Pain Or Diseases':
        prompt_medical_field = 'chronic pain or disease'
    return prompt_device_name, prompt_medical_field


def create_single_prompt(trials, start_trial, last_trial, device_name, medical_field, output_length, multiple_batch_indicator, write):
    #if multiple_batch_indicator == '':
    #    trials, start_trial, last_trial = integrate_manufacturer_trials(trials, device_name, medical_field, write)

    prompt_device_name, prompt_medical_field = get_prompt_variables(device_name, medical_field)

    if last_trial == start_trial:
        prompt = f'''Your task is to extract relevant information from the inputted trial labeled {start_trial} to construct an argument about the purpose of {prompt_device_name} in {prompt_medical_field} trials. The trial contains a title and description. Your reader will be clinical research coordinators.
---
Trial:
{trials[:-1]}
---
Task: Write a {output_length}-word thesis about the purpose of {prompt_device_name} in {prompt_medical_field} trials with in-line references to the trial in the following format: [{start_trial}].
        '''
        return prompt

    prompt = f'''Your task is to extract relevant information from the {last_trial - start_trial + 1} inputted trials labeled from {start_trial} to {last_trial} to construct an argument about the purpose of {prompt_device_name} in {prompt_medical_field} trials. Each trial contains a title and description. Your reader will be clinical research coordinators.
---
Trials:
{trials[:-1]}
---
Task: Write a {output_length}-word thesis about the purpose of {prompt_device_name} in {prompt_medical_field} trials with in-line references to the trials in the following format: [{start_trial}].'''
    return prompt


def create_summaries_prompt(topic, dict, output_length, folder):
    summaries = ''
    reg = re.match('(.*)_(.*)', topic)
    device_name = reg.group(1)
    medical_field = reg.group(2)
    prompt_device_name, prompt_medical_field = get_prompt_variables(device_name, medical_field)
    summary_index = 0
    for num in dict[topic]:
        summary_index += 1
        summaries += f'Summary {summary_index}. {get_file_contents(f"{folder}/{topic}{num}.txt")}\n\n\n'
        #summaries += f'Summary {summary_index}. {get_file_contents(f"{folder}/{topic}{num}.txt")}\n\n\n'

    prompt = f'''Your task is to extract relevant information from the {summary_index} inputted summaries labeled from 1 to {summary_index} to construct an argument about the purpose of {prompt_device_name} in {prompt_medical_field} trials.
Each summary includes in-line references to clinical trials in the following format: [1]. Your reader will be clinical research coordinators.
---
Summary:
{summaries}
---
Task: Write a concise {output_length}-word thesis about the purpose of {prompt_device_name} in {prompt_medical_field} trials. Use the numeric in-line citation format [1], [2], etc., to reference sources as appropriate. '''
    return prompt


def trim_response(response):
    start = 0
    end = len(response)
    if 'Thesis:' in response:
        start = 8
    if 'References:' in response:
        end = response.find('References:')
    response = response[start:end].strip()
    return response


def check_response(response, output_length):
    response = trim_response(response)
    word_count = len(response.split(' '))
    reg = re.match('(\d*)-(\d*)', output_length)
    min_length = int(reg.group(1))
    max_length = int(reg.group(2))
    if word_count < min_length:
        return f'{min_length + 50}-{max_length}'
    elif word_count > max_length:
        return f'{max(min_length - 50, 50)}-{max_length - 50}'
    return ''


def summarize_folder(input_folder):
    def has_number(s):
        for char in s:
            if char.isdigit():
                return True
        return False
    folder_files = os.listdir('' + input_folder)
    #folder_files = os.listdir(input_folder)
    output_folder = f'{input_folder[:15]}devices_gpt_output/'
    #output_folder = f'devices_gpt_output/'
    repeat_files = [match for match in folder_files if has_number(match[-5:])]
    for file in folder_files:
        output_length = '150-250'
        match = re.match('(.*)_([A-Za-z]*)(\d)*.txt', file)
        device_name = match.group(1)
        medical_field = ' '.join(re.findall('[A-Z][a-z]*', match.group(2)))
        index = match.group(3)
        multiple_batch_indicator = ''

        if os.path.getsize(f'{input_folder}/{file}') == 0:
        #if os.path.getsize(f'{input_folder}/{file}') == 0:
            with open(f'{output_folder + device_name}_{"".join(medical_field.split(" "))}.txt', 'w', encoding = 'utf-8') as outfile:
                pass
            continue

        if file in repeat_files:
            output_length = '450-550'
            multiple_batch_indicator = str(index)

        trials = get_file_contents(f'{input_folder}/{file}')
        #trials = get_file_contents(f'{input_folder}/{file}')
        start_trial = int(re.match('(\d+).*', trials).group(1))
        last_trial = int(re.search(':eltiT \.(\d+)', trials[::-1], re.DOTALL).group(1)[::-1])

        if last_trial - start_trial + 1 <= 5:
            output_length = '50-150'

        prompt = create_single_prompt(trials, start_trial, last_trial, device_name, medical_field, output_length, multiple_batch_indicator, True)
        response = get_completion(prompt)

        response_valid = check_response(response, output_length)
        if response_valid != '':
            prompt = create_single_prompt(trials, start_trial, last_trial, device_name, medical_field, response_valid, multiple_batch_indicator, False)
            response = get_completion(prompt)
            response = trim_response(response)

        current_date = datetime.datetime.now().strftime('%Y-%m-%d')

        output = f'Date: {current_date}\n\n{response}'
        if multiple_batch_indicator != '':
            output = response

        with open(f'{output_folder + device_name}_{"".join(medical_field.split(" ")) + multiple_batch_indicator}.txt',
                  'w', encoding = 'utf-8') as outfile:
            outfile.write(output)
    return repeat_files


def rerun(input_folder, dict):
    output_length = '150-250'

    for topic, indexes in dict.items():
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        reg = re.match('(.*)_(.*)', topic)
        device_name = reg.group(1)
        medical_field = reg.group(2)
        prompt = create_summaries_prompt(topic, dict, output_length, input_folder)
        response = get_completion(prompt)
        response = trim_response(response)
        response_valid = check_response(response, '150-300')
        if response_valid != '':
            prompt = create_summaries_prompt(topic, dict, response_valid, input_folder)
            response = get_completion(prompt)
            response = trim_response(response)
        output = f'Date: {current_date}\n\n{response}'
        with open(f'{input_folder}/{device_name}_{"".join(medical_field.split(" "))}.txt', 'w', encoding = 'utf-8') as outfile:
        #with open(f'{input_folder}/{device_name}_{"".join(medical_field.split(" "))}.txt',
        #          'w', encoding = 'utf-8') as outfile:
            outfile.write(output)


def remove_old_files(reference_folder):
    try:
        for filename in os.listdir(reference_folder):
            full_path = os.path.join(reference_folder, filename)
            if filename[-5].isdigit():
                os.remove(full_path)
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    if len(sys.argv) < 2:
        print('Usage: python Gpt.py <folder1>')
        return

    input_folder = sys.argv[1]

    config = read_config()
    openai.api_key = config.get('OpenAIAPI', 'key')
    openai_model = config.get('OpenAIAPI', 'model')
    
    repeat_topics = summarize_folder(input_folder)
    pattern = re.compile(r'(.*)(\d)\.txt')
    dict = {}

    
    for match in repeat_topics:
        match_result = pattern.search(match)
        topic = match_result.group(1)
        number = match_result.group(2)
        if topic in dict:
            dict[topic].append(number)
        else:
            dict[topic] = [number]
    
    summary_folder = input_folder[:14] + '/devices_gpt_output'
    rerun(summary_folder, dict)
    remove_old_files(summary_folder)


if __name__ == '__main__':
    main()
