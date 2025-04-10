from util import *
import sys
import subprocess


def print_list(input):
    print("\n".join(item for item in input))


def print_numbered_list(input):
    print("0. Cancel")
    for i, option in enumerate(input, start = 1):
        print(f"{i}. {option}")


def print_dict(input):
    for key, val in input.items():
        print(f"{key}: {val}")


def user_input(options):
    while True:
        try:
            user_choice = int(input("Enter the number of your choice: "))
            if user_choice == 0:
                sys.exit(0)
            elif 1 <= user_choice <= len(options):
                return user_choice
            else:
                print(f"Invalid input. Please enter a number between 0 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def prompt_user_for_first_options(first_options):
    print("You are attempting to make changes! Would you like to see current values or change pipeline values? Please choose an option:")

    print_numbered_list(first_options)
    return user_input(first_options)
        

def check_exists(existing, new_addition):
    if new_addition == '0':
        sys.exit(0)
    if new_addition == '':
        raise Exception("Cannot input an empty string")
    return new_addition in existing



def write_config():
    config["MedicalFields"]["file_fields"] = ', '.join(config_dict["Medical File Fields"])
    config["MedicalFields"]["text_fields"] = ', '.join(config_dict["Medical Text Fields"])
    config["Devices"]["devices"] = ', '.join(config_dict["Devices"])
    
    for key, value in config_dict["Search Terms"].items():
        config.set("AlgSearchTerms", key, value)

    for key, value in config_dict["Formatted Search Terms"].items():
        config.set("FormattedAlgSearchTerms", key, value)

    with open('internal_files/config.ini', 'w') as configfile:
        config.write(configfile)


def add_to_dict(dict_key, word_to_add):
    config_dict[dict_key].append(word_to_add)
    config_dict[dict_key].sort()


def remove_from_dict(dict_key, index_to_remove):
    config_dict[dict_key].pop(index_to_remove)


def change_in_dict(dict_key, index, new_string):
    config_dict[dict_key][index] = new_string
    config_dict[dict_key].sort()


def get_user_medical_field(message):
    return str(input(message)).strip().capitalize()


def get_user_device(message):
    input_device = str(input(message)).strip()
    return "_".join(input_device.split())


def get_user_search_term(message):
    return str(input(message)).strip().lower()


def get_all_user_search_terms(device_string, action_word):
    search_term_list = []
    new_search_term = get_user_search_term(f"Which search terms would you like to use to find this device? Type them in one at a time: ")
    while(new_search_term != '0'):
        if new_search_term != '' and new_search_term not in search_term_list:
            search_term_list.append(new_search_term)
        new_search_term = get_user_search_term(f"Next search term: ")
    
    if len(search_term_list) == 0: # Exit without adding new device
        print(f"\nERROR!\n{device_string} will not be {action_word} since no search terms were defined.")
        sys.exit(0)

    fourth_list = ['Change Search Terms', 'Confirm Additions']
    print(f"The search terms defined for {device_string} are the following: {search_term_list}.")
    print_numbered_list(fourth_list)
    chosen_index = user_input(fourth_list)
    return chosen_index, search_term_list


def see_pipeline_values():
    print("\nWhat values would you like to see? Please choose an option:")
    print_numbered_list(second_options)
    chosen_index = user_input(second_options)
    if chosen_index == 1:
        print(f"\nHere are the current {second_options[chosen_index - 1].lower()}:")
        print_list(config_dict["Medical File Fields"])
    elif chosen_index == 2:
        print(f"\nHere are the current {second_options[chosen_index - 1].lower()}:")
        print_list(config_dict[second_options[chosen_index - 1]])
    else:
        print("\nWould you like to see a specific device's search terms or all of the search terms?")
        
        print_numbered_list(search_term_options)
        chosen_index = user_input(search_term_options)

        if chosen_index == 1:
            print(f"\nHere are the current devices:")
            print_numbered_list(config_dict['Devices'])
            print("\nWhat device would you like search terms for?")
            chosen_index = user_input(config_dict['Devices']) - 1

            chosen_device = config_dict['Devices'][chosen_index]
            
            print(f"\nSearch terms for {chosen_device}:")
            search_terms = config_dict["Formatted Search Terms"][chosen_device]
            print_list(search_terms.split(', '))

        else:
            print(f"\nHere are the current search terms:")
            print_dict(config_dict["Formatted Search Terms"])


def run_clear_master_lists():
    command = ['sbatch', 'helpful_files/RestartMasterLists.sh']
    try:
        subprocess.run(command, check=True)
        print("Script submitted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to submit script: {e}")


def handle_medical_field_modification(third_options):
    print(f"\nHere are the current medical fields:")
    print_list(config_dict["Medical Text Fields"])
    print(f"\nWould you like to add a medical field, change a medical field, or delete a medical field?")
    print_numbered_list(third_options)
    category_chosen_index = chosen_index
    action_chosen_index = user_input(third_options)

    if action_chosen_index == 1: #Add Medical Field
        message_for_user = f"\nWhich medical field would you like to add? Note: Capitalize as if you are writing the medical field in a sentence. Ex: Cardiology or General Physiology.\nInput 0 if you want to cancel.\n"
        input_string = get_user_medical_field(message_for_user)
        while check_exists(config_dict["Medical Text Fields"], input_string):
            print("The inputted medical field already exists!")
            input_string = get_user_medical_field(message_for_user)
        add_to_dict("Medical Text Fields", input_string)
        add_to_dict("Medical File Fields", input_string.title())
        run_clear_master_lists()
        write_config()
        print(f"'{input_string}' added!")

    elif action_chosen_index == 2: #Change Medical Field
        print("\nHere are the existing medical fields:")
        print_numbered_list(config_dict["Medical Text Fields"])
        print("Which medical field would you like to change?")
        chosen_field_index = user_input(config_dict["Medical Text Fields"]) - 1
        chosen_field = config_dict['Medical Text Fields'][chosen_field_index]
        message_for_user = f"\nWhat would you like to replace \'{chosen_field}\' with? Note: Capitalize as if you are writing the medical field in a sentence. Ex: Cardiology or General Physiology.\nInput 0 if you want to cancel. "
        input_string = get_user_medical_field(message_for_user)
        while check_exists(config_dict["Medical Text Fields"], input_string):
            print("The inputted medical field already exists!")
            input_string = get_user_medical_field(message_for_user)
        change_in_dict("Medical Text Fields", chosen_field_index, input_string)
        change_in_dict("Medical File Fields", chosen_field_index, input_string.title())
        run_clear_master_lists()
        write_config()
        print(f"{chosen_field} replaced with {input_string}!")

    else: #Delete Medical Field
        print("")
        print_numbered_list(config_dict["Medical Text Fields"])
        chosen_field_index = user_input(config_dict["Medical Text Fields"]) - 1
        chosen_field = config_dict['Medical Text Fields'][chosen_field_index]
        remove_from_dict("Medical Text Fields", chosen_field_index)
        remove_from_dict("Medical File Fields", chosen_field_index)
        write_config()
        print(f"'{chosen_field}' removed!")


def remake_past_devices_json():
    current_devices = config_dict["Devices"]
    with open('internal_files/Devices.json', encoding = 'utf8') as past_devices_json:
        data = json.load(past_devices_json)

        for device in list(data.keys()):
            if device not in current_devices:
                del data[device]
        
        for device in current_devices:
            if device not in data:
                data[device] = [0]

        data = dict(sorted(data.items()))

        conversion(data, 'internal_files/Devices.json')

    with open('helpful_files/PastDevices.json', encoding = 'utf8') as past_devices_json:
        data = json.load(past_devices_json)

        for device in list(data.keys()):
            if device not in current_devices:
                del data[device]
        
        for device in current_devices:
            if device not in data:
                data[device] = [0]

        data = dict(sorted(data.items()))

        conversion(data, 'helpful_files/PastDevices.json')


def add_to_devices_master_lists(device_name):
    new_file_name = f'devices_master_lists/{device_name}.json'
    prototype_file = f'helpful_files/Template.json'
    with open(prototype_file, 'r') as src:
        contents = src.read()
    with open(new_file_name, 'w') as dest:
        dest.write(contents)


def change_devices_master_lists(old_device_name, new_device_name):
    new_file_name = f'devices_master_lists/{new_device_name}.json'
    old_file_name = f'devices_master_lists/{old_device_name}.json'
    os.rename(old_file_name, new_file_name)


def remove_devices_master_list(old_device_name):
    old_file_name = f'devices_master_lists/{old_device_name}.json'
    os.remove(old_file_name)


def update_search_terms(device_name, old_search_term_list, to_be_added):
    all_search_terms = [key for key in config_dict["Search Terms"]]

    new_search_term_list = old_search_term_list

    for search_term in to_be_added:
        if search_term not in new_search_term_list:
            if search_term in all_search_terms:
                config_dict["Search Terms"][search_term] += f', {device_name}'
                new_search_term_list.append(search_term)
            else:
                config_dict["Search Terms"][search_term] = device_name
                new_search_term_list.append(search_term)
    return new_search_term_list


def handle_device_modification(third_options):
    print(f"\nHere are the current devices:")
    print_list(config_dict["Devices"])
    print(f"\nWould you like to add a device, change a device, or delete a device?")
    print_numbered_list(third_options)
    action_chosen_index = user_input(third_options)

    if action_chosen_index == 1: #Add Device
        message_for_user = f"\nWhich device would you like to add? Note: Capitalize as if you are writing the device name in a sentence. Ex: Google.\nInput 0 if you want to cancel.\n"
        device_string = get_user_device(message_for_user)
        while check_exists(config_dict["Devices"], device_string):
            print("The inputted device already exists!")
            device_string = get_user_device(message_for_user)
        print(f"\nIn order to integrate '{device_string}' into the pipeline, you need to define what search terms will be used to find the device.")
        print(f"If a space is required at the beginning or end of the search term, input '_' where the space should go. Example: 'strava ' should be input as 'strava_'.")
        print(f"When you are done inputting search terms, enter a '0'.")

        chosen_index, search_term_list = get_all_user_search_terms(device_string, "added")
        while chosen_index == 1:
            chosen_index, search_term_list = get_all_user_search_terms(device_string, "added")

        add_to_dict("Devices", device_string)

        search_term_list = update_search_terms(device_string, [], search_term_list)

        config_dict["Search Terms"] = dict(sorted(config_dict["Search Terms"].items(), key=lambda item: (item[1], item[0])))
        config_dict["Formatted Search Terms"][device_string] = ", ".join(search_term_list)

        add_to_devices_master_lists(device_string)

        print(f"'{device_string}' with search terms: {search_term_list} added!")
    
    elif action_chosen_index == 2: #Change Device
        print("\nHere are the existing devices:")
        print_numbered_list(config_dict["Devices"])
        print("Which device would you like to change?")
        chosen_device_index = user_input(config_dict["Devices"]) - 1
        chosen_device = config_dict['Devices'][chosen_device_index]
        message_for_user = f"\nWhat would you like to replace \'{chosen_device}\' with? Note: Capitalize as if you are writing the device in a sentence. Ex: Apple HealthKit or Google.\nInput 0 if you want to cancel. "
        input_string = get_user_device(message_for_user)
        while check_exists(config_dict["Devices"], input_string):
            print("The inputted device already exists!")
            input_string = get_user_device(message_for_user)
        change_in_dict("Devices", chosen_device_index, input_string)

        for search_term in config_dict["Formatted Search Terms"][chosen_device].split(", "):
            if len(config_dict["Search Terms"][search_term].split(', ')) > 1:
                current_devices = config_dict["Search Terms"][search_term].split(', ')
                updated_devices = [device if device != chosen_device else input_string for device in current_devices]
                config_dict["Search Terms"][search_term] = ', '.join(updated_devices)
            else:
                config_dict["Search Terms"][search_term] = input_string

        config_dict["Formatted Search Terms"][input_string] = config_dict["Formatted Search Terms"][chosen_device]  
        del config_dict["Formatted Search Terms"][chosen_device]

        config.remove_option("FormattedAlgSearchTerms", chosen_device)

        change_devices_master_lists(chosen_device, input_string)

        print(f"{chosen_device} replaced with {input_string}!")

    else: #Delete Device
        print("")
        print_numbered_list(config_dict["Devices"])
        chosen_device_index = user_input(config_dict["Devices"]) - 1
        chosen_device = config_dict['Devices'][chosen_device_index]

        remove_from_dict("Devices", chosen_device_index)

        for search_term in config_dict["Formatted Search Terms"][chosen_device].split(", "):
            if len(config_dict["Search Terms"][search_term].split(', ')) > 1:
                current_devices = config_dict["Search Terms"][search_term].split(', ')
                updated_devices = [device for device in current_devices if device != chosen_device]
                config_dict["Search Terms"][search_term] = ', '.join(updated_devices)
            else:
                del config_dict["Search Terms"][search_term]
                config.remove_option("AlgSearchTerms", search_term)

        del config_dict["Formatted Search Terms"][chosen_device]
        config.remove_option("FormattedAlgSearchTerms", chosen_device)

        remove_devices_master_list(chosen_device)

        print(f"'{chosen_device}' removed!")

    write_config()
    remake_past_devices_json()


def handle_search_term_modification(third_options):
    print(f"\nHere are the current search terms:")
    print_dict(config_dict["Formatted Search Terms"])
    print(f"\nWould you like to add a search term, change a search term, or delete a search term?")
    print_numbered_list(third_options)
    action_chosen_index = user_input(third_options)

    if action_chosen_index == 1: #Add Search Terms
        print("\nHere are the existing devices:")
        print_numbered_list(config_dict["Devices"])
        print("Which device would you like to add a search term to?")
        chosen_device_index = user_input(config_dict["Devices"]) - 1
        chosen_device = config_dict['Devices'][chosen_device_index]

        print(f"\nCurrent search terms for {chosen_device}:")
        search_terms = config_dict["Formatted Search Terms"][chosen_device]
        old_search_term_list = search_terms.split(', ')
        print_list(old_search_term_list)

        print(f"What search terms do you want to add?")
        print(f"If a space is required at the beginning or end of the search term, input '_' where the space should go. Example: 'strava ' should be input as 'strava_'.")
        print(f"When you are done inputting search terms, enter a '0'.")

        chosen_index, search_term_list = get_all_user_search_terms(chosen_device, "added")
        while chosen_index == 1:
            chosen_index, search_term_list = get_all_user_search_terms(chosen_device, "added")

        all_search_terms = [key for key in config_dict["Search Terms"]]

        new_search_term_list = update_search_terms(chosen_device, old_search_term_list, search_term_list)

        new_search_term_list = sorted(new_search_term_list)

        print(f"'{chosen_device}' with search terms: {new_search_term_list} updated!")

        for search_term in new_search_term_list:
            config_dict["Search Terms"][search_term] = chosen_device

        config_dict["Formatted Search Terms"][chosen_device] = ', '.join(new_search_term_list)

        write_config()

    elif action_chosen_index == 2: #Change Search Terms
        print("\nHere are the existing devices:")
        print_numbered_list(config_dict["Devices"])
        print("Which device would you like to change the search terms of?")
        chosen_device_index = user_input(config_dict["Devices"]) - 1
        chosen_device = config_dict['Devices'][chosen_device_index]

        print(f"\nCurrent search terms for {chosen_device}:")
        search_terms = config_dict["Formatted Search Terms"][chosen_device]
        old_search_term_list = search_terms.split(', ')
        print_list(old_search_term_list)

        print(f"What would you like the new search terms to be?")
        print(f"If a space is required at the beginning or end of the search term, input '_' where the space should go. Example: 'strava ' should be input as 'strava_'.")
        print(f"When you are done inputting search terms, enter a '0'.")

        chosen_index, search_term_list = get_all_user_search_terms(chosen_device, "changed")
        while chosen_index == 1:
            chosen_index, search_term_list = get_all_user_search_terms(chosen_device, "changed")

        all_search_terms = [key for key, val in config_dict["Search Terms"].items() if val != chosen_device]

        if len(search_term_list) == 0:
            print("You cannot input 0 accepted search terms. If you want to delete a device, do so by re-running this script and going through device.")
        
        else:
            for search_term in old_search_term_list:
                if len(config_dict["Search Terms"][search_term].split(', ')) > 1:
                    current_devices = config_dict["Search Terms"][search_term].split(', ')
                    updated_devices = [device for device in current_devices if device != chosen_device]
                    config_dict["Search Terms"][search_term] = ', '.join(updated_devices)
                else:
                    del config_dict["Search Terms"][search_term]
                    config.remove_option("AlgSearchTerms", search_term)

            new_search_term_list = update_search_terms(chosen_device, [], search_term_list)
            new_search_term_list = sorted(new_search_term_list)
            config_dict["Formatted Search Terms"][chosen_device] = ', '.join(new_search_term_list)

            print(f"'{chosen_device}' with search terms: {search_term_list} updated!")

        write_config()   

    else: # Delete Search Terms
        print("\nHere are the existing devices:")
        print_numbered_list(config_dict["Devices"])
        print("Which device would you like to change the search terms of?")
        chosen_device_index = user_input(config_dict["Devices"]) - 1
        chosen_device = config_dict['Devices'][chosen_device_index]

        print(f"\nCurrent search terms for {chosen_device}:")
        search_terms = config_dict["Formatted Search Terms"][chosen_device]
        old_search_term_list = search_terms.split(', ')

        if len(old_search_term_list) == 1:
            print_list(old_search_term_list)            
            print("You cannot delete any search terms from this device since there is only one current search term. \nRe-run this script if you would like to change the search terms, add search terms, or delete this device.")
        else:
            print_numbered_list(old_search_term_list)

            chosen_term_index = user_input(config_dict["Devices"]) - 1
            chosen_term = config_dict['Formatted Search Terms'][chosen_device].split(", ")[chosen_term_index]

            old_search_term_list.pop(chosen_term_index)
            if len(config_dict["Search Terms"][chosen_term].split(', ')) > 1:
                current_devices = config_dict["Search Terms"][chosen_term].split(', ')
                updated_devices = [device for device in current_devices if device != chosen_device]
                config_dict["Search Terms"][chosen_term] = ', '.join(updated_devices)
            else:
                del config_dict["Search Terms"][chosen_term]
                config.remove_option("AlgSearchTerms", chosen_term)

            new_search_term_list = old_search_term_list

            config_dict["Formatted Search Terms"][chosen_device] = ", ".join(new_search_term_list)

            write_config()
            print(f"'{chosen_term} removed from {chosen_device}' search terms!")


def change_pipeline_values():
    print("\nCAUTION!!! Changing values will force re-runs of summaries, which will cost money.")
    print("What values would you like to change? If you would like to not change any values, input 0. Please choose an option:")
    print_numbered_list(second_options)
    chosen_index = user_input(second_options)
    third_options = ['Add', 'Change', 'Delete']

    if chosen_index == 1:
        handle_medical_field_modification(third_options)

    elif chosen_index == 2:
        handle_device_modification(third_options)

    else:
        handle_search_term_modification(third_options)


if __name__ == "__main__":
    config = read_config()
    config_dict = {
    "Medical Text Fields" : config.get("MedicalFields", "text_fields").split(', '),
    "Medical File Fields" : config.get("MedicalFields", "file_fields").split(', '),
    "Devices" : config.get("Devices", "devices").split(', '),
    "Search Terms" : config.items("AlgSearchTerms"),
    "Formatted Search Terms": config.items('FormattedAlgSearchTerms'),
    }

    config_dict["Search Terms"] = {key : value for key, value in config_dict["Search Terms"]}
    config_dict["Formatted Search Terms"] = {key : value for key, value in config_dict["Formatted Search Terms"]}

    first_options = ["See current values", "Change pipeline values"]
    second_options = ["Medical Fields", "Devices", "Search Terms"]
    search_term_options = ["Specific device", "All"]

    chosen_index = prompt_user_for_first_options(first_options)
    if chosen_index == 1:
        see_pipeline_values()

    else:
        change_pipeline_values()
