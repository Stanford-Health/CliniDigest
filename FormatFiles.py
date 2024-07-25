import json
import math
import regex as re
import sys
import tiktoken


def num_tokens_from_string(string: str, encoding_name: str):
    '''Returns the number of tokens in a text string.'''
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def output_files(filename, medical_fields):
    with open(filename, encoding = 'utf-8') as f:
        data = json.load(f)
        for medical_field in medical_fields:
            key_trials = data[medical_field][0]
            print(len(data[medical_field]))
            output = ''
            reference_list = []
            for i in range(1, key_trials + 1):
                reference = data[medical_field][i][0]
                title = data[medical_field][i][1]
                body = data[medical_field][i][2]
                reference_list.append(f'[{i}]. {reference}')
                output += f'{i}. Title: {title}\nDescription: {body}\n'
            if ' ' in medical_field:
                medical_field = medical_field.replace(' ', '')
            if '/' in medical_field:
                medical_field = medical_field.replace('/', 'Or')
            device = re.match('devices_master_lists/(.*).json', filename).group(1)
            token_length = num_tokens_from_string(output, 'cl100k_base')

            if token_length < 120000:
                with open(f'internal_files/devices_gpt_input/{device}_{medical_field}.txt', 'w') as outfile:
                    outfile.write(output)
            else: 
                num_files = math.ceil(token_length/15000)
                num_trials = math.ceil(key_trials/num_files)
                start = 0
                end = 0
                for i in range(1, num_files + 1):
                    with open(f'internal_files/devices_gpt_input/{device}_{medical_field}{i}.txt', 'w', encoding='utf-8') as outfile:
                        index = i * (num_trials - 1) + 1
                        if index >= key_trials:
                            end = len(output)
                        else:
                            end = output.index(f'{index}. Title: ')
                        temp = output[start:end]
                        outfile.write(output[start:min(end, len(output))])
                        start = end
            with open(f'internal_files/devices_references/{device}_{medical_field}.txt', 'w') as outfile:
                    outfile.writelines('\n'.join(reference_list))


def main():
    if len(sys.argv) < 2:
        print('Usage: python Filter.py <file1>')
        return

    filename1 = sys.argv[1]
    with open(f'internal_files/{filename1}', encoding = 'utf-8') as f:
        data = json.load(f)
        for device in data:
            medical_fields = data[device]
            output_files(f'devices_master_lists/{device}.json', medical_fields)

if __name__ == '__main__':
    main()

