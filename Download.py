import json
import subprocess
from datetime import datetime, timedelta
from util import *


def search_devices(study, data, Dict_to_add):
    if isinstance(data, dict):
        for key, value in data.items():
            search_devices(study, value, Dict_to_add)
    elif isinstance(data, list):
        for item in data:
            search_devices(study, item, Dict_to_add)
    elif isinstance(data, str):
        for search_term in alg_search_terms:
            if search_term in data.lower():
                array_to_add = ['https://clinicaltrials.gov/study/' + study["identificationModule"]["nctId"], study["identificationModule"]["briefTitle"], study["descriptionModule"]["briefSummary"]]
                device_name = alg_search_terms[search_term]
                if array_to_add not in Dict_to_add[device_name]:
                    Dict_to_add[device_name][0] += 1
                    Dict_to_add[device_name].append(array_to_add)
 
                   
def curl(base_url, url, Device_Dict):
    try:
        result = subprocess.check_output(['curl', url], text=True, encoding='utf-8')
        data = json.loads(result)
        for study in data['studies']:
            search_devices(study['protocolSection'], study, Device_Dict)
        if 'nextPageToken' in data:
            next_page_token = data['nextPageToken']
            url = base_url + '&pageToken=' + next_page_token
            return curl(base_url, url, Device_Dict)
        else:
            return Device_Dict

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def main():
    config = read_config()

    global devices 
    global alg_search_terms
    devices = config.get('Devices', 'devices').split(', ')
    alg_search_terms = {}
    for key, value in config.items('AlgSearchTerms'):
        if '_' in key:
            alg_search_terms[key.replace('_', ' ')] = value
        else:
            alg_search_terms[key] = value
    
    Device_Dict = {}
    for device in devices:
        Device_Dict.update({device : [0]})
    
    
    #new trials
    current_date = datetime.now()
    left_date = (current_date - timedelta(days=(365 * 2))).strftime("%Y-%m-%d")
    right_date = '+MAX'
    base_url = (rf"https://clinicaltrials.gov/api/v2/studies?query.term=AREA%5BLastUpdatePostDate%5DRANGE%5B{left_date}%2C{right_date}%5D+AND+AREA%5BEnrollmentCount%5DRANGE%5B30%2CMAX%5D&postFilter.overallStatus=RECRUITING%7CENROLLING_BY_INVITATION%7CACTIVE_NOT_RECRUITING%7CNOT_YET_RECRUITING%7CSUSPENDED%7CCOMPLETED&sort=LastUpdatePostDate&pageSize=1000")
    Device_Dict = curl(base_url, base_url, Device_Dict)

    #current trials
    left_date = (current_date - timedelta(days = 5 * 365)).strftime("%Y-%m-%d")
    right_date = (current_date - timedelta(days=(365 * 2 + 1))).strftime("%Y-%m-%d")
    base_url = (rf"https://clinicaltrials.gov/api/v2/studies?query.term=AREA%5BLastUpdatePostDate%5DRANGE%5B{left_date}%2C{right_date}%5D+AND+AREA%5BEnrollmentCount%5DRANGE%5B30%2CMAX%5D&postFilter.overallStatus=RECRUITING%7CENROLLING_BY_INVITATION%7CACTIVE_NOT_RECRUITING&sort=LastUpdatePostDate&pageSize=1000")
    Device_Dict = curl(base_url, base_url, Device_Dict)
    
    conversion(Device_Dict, r'internal_files/Devices.json')

if __name__ == '__main__':
    main()
