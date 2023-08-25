from bs4 import BeautifulSoup
import json
import os
from util import *

field_names = ['agency',
               'arm_group',
               'brief_summary', 
               'brief_title',
               'condition', 
               'description', 
               'descriptions', 
               'detailed_description',
               'intervention',
               'keyword',
               'official_title',
               'other_outcome', 
               'primary_outcome', 
               'secondary_outcome',
               'study_design_info' 
               ]

device_search_terms = {
    'Actigraph_CentrePoint_Insight': {'centrepoint insight'},
    'Apple_Watch_5': {'apple watch series 5', 'apple watch series'},
    'Biostrap_Evo': {'biostrap evo'},
    'Coros_Pace': {'coros pace'},
    'Cronometer': {'cronometer'},
    'Dexcom_G6_Pro': {'dexcom g6 pro', 'dexcom g6pro'},
    'Dreem_Headband_3': {'dreem headband 3', 'dreem headband', 'dreem 3', 'dreem'},
    'Fitbit_Charge_4': {'fitbit charge 4'},
    'Fitbit_Sense': {'fitbit sense'},
    'Garmin_Fenix_7S': {'garmin watch', 'garmin smart watch', 'garmin smartwatch'},
    'Google_Fit': {'google fit', 'googlefit'},
    'MyFitnessPal': {'myfitnesspal', 'my fitness pal', 'myfitness pal'},
    'Nutrisense_CGM': {'nutrisense cgm'},
    'Oura_Ring_Gen_3': {'oura ring'},
    'Polar_H10': {'polar h10'},
    'Polar_Vantage_V2': {'polar vantage'},
    'Polar_Verity_Sense': {'polar verity sense'},
    'SleepOn_Go2Sleep': {'sleepon go2sleep'},
    'Strava': {' strava'},
    'Suuntu_9_Peak_Pro': {'suuntu 9'},
    'Suuntu_HR_Belt': {'suuntu hr belt'},
    'Whoop_Strap_4.0': {'whoop '},
    'Withings_Body+': {'withings body+'},
    'Withings_ScanWatch': {'withings scanwatch'},
    'Withings_Sleep': {'withings sleep'}
}

manufacturer_search_terms = {
    'Actigraph': [True, {'ActiGraph'}], #requires capitalization
    'Apple': [False, {'apple watch'}],
    'Biostrap': [False, {'biostrap'}],
    'Coros': [True, {'COROS'}], #requires capitalization
    'Cronometer': [False, {'cronometer'}], 
    'Dexcom': [False, {'dexcom'}], 
    'Dreem': [False, {'dreem'}], 
    'Fitbit': [False, {'fitbit'}], 
    'Garmin': [False, {'garmin'}],
    'Google': [False, {'google'}], 
    'MyFitnessPal': [False, {'myfitnesspal', 'my fitness pal', 'myfitness pal'}],
    'Nutrisense': [False, {'nutrisense'}],
    'Oura': [False, {'oura '}], 
    'Polar': [False, {'polar ignite', 'polar pacer', 'polar vantage', 'polar grit', 'polar unite', 'polar verity', 'polar h'}],
    'SleepOn': [False, {'sleepon '}],
    'Strava': [False, {' strava'}],
    'Suuntu': [False, {'suuntu'}],
    'Whoop': [True, {'WHOOP', 'whoop ', 'Whoop '}], #requies capitalization
    'Withings': [False, {'withings'}]
}

return_value_tags = {
    'url': False,
    'brief_title': False,
    'enrollment': False,
    'overall_status': False,
    'start_date': False,
    'last_update_posted': False,
    'study_type': False,
    'condition': True,
    'keyword': True, 
    'brief_summary': False
}

def get_vals(soup, term, multiple):
    if soup.find(term) is None:
        return None
    else:
        if not multiple:
            if term != 'brief_summary':
                return soup.find(term).text
            else:
                return ' '.join(soup.find(term).text.split())
        else: 
            return tuple(word.text for word in soup.find_all(term))


def search_devices(contents, soup, Dict_to_add, search_terms):
    for key, value in search_terms.items():
        contents = contents.lower()
        for term in value:
            if contents.find(term) != -1: 
                array_to_add = []
                for tag, multiple in return_value_tags.items():
                    array_to_add.append(get_vals(soup, tag, multiple))
                if array_to_add not in Dict_to_add[key]:
                    Dict_to_add[key][0] += 1
                    Dict_to_add[key].append(array_to_add) 
                break


def search_manufacturers(contents, soup, Dict_to_add, search_terms):
    for key, value in search_terms.items():
        if not value[0]:
            contents = contents.lower()
        for term in value[1]:
            if contents.find(term) != -1: 
                array_to_add = []
                for tag, multiple in return_value_tags.items():
                    array_to_add.append(get_vals(soup, tag, multiple))
                if array_to_add not in Dict_to_add[key]:
                    Dict_to_add[key][0] += 1
                    Dict_to_add[key].append(array_to_add) 
                break


def main():
    Device_Dict = {}
    Manufacturer_Dict = {}
    for device in device_search_terms:
        Device_Dict.update({device : [0]})
    for manufacturer in manufacturer_search_terms:
        Manufacturer_Dict.update({manufacturer : [0]})
    
    
    for folder in os.scandir('.'):
        if folder.is_dir():
            for file in os.scandir(folder.path):
                with open(file, 'r', encoding = 'utf-8') as f:
                    data = f.read()

                    soup = BeautifulSoup(data, 'xml')
                    contents = ''
                    for i in field_names:
                        for found in soup.findAll(i):
                            contents += found.text + ' '

                    contents = ' '.join(contents.split())
                    search_devices(contents, soup, Device_Dict, device_search_terms)
                    search_manufacturers(contents, soup, Manufacturer_Dict, manufacturer_search_terms)
    
    conversion(Device_Dict, input_output_folder + 'MainDevices.json')
    conversion(Manufacturer_Dict, input_output_folder + 'MainManufacturers.json')

if __name__ == '__main__':
    main()
 
