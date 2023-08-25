import json
import os
from util import *


def filter(inputFile, outputFile):
    with open(inputFile, encoding = 'utf8') as JSONFILE:
        data = json.load(JSONFILE)

        for key, value in data.items():
            device_num = value[0]
            for i in range(1, device_num + 1):
                value[i] = value[i][:-1]
    conversion(data, outputFile)


def main():
    filter(input_output_folder + 'MainDevices.json', 
           input_output_folder + 'WebsiteDevices.json')
    filter(input_output_folder + 'MainManufacturers.json',
           input_output_folder + 'WebsiteManufacturers.json')


if __name__ == '__main__':
    main() 
