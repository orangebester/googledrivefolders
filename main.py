import requests
import time
import json
import sys
import random
import string

from personal_data import template_spreadsheet_id
from folder_tree import create_folder_tree
from google_service import service


def generate_id():
    """ Generates id each elements of which consist of random values """
    alphabet = list(string.ascii_lowercase)
    first = random.randint(0, 9)
    second = random.choice(alphabet)
    third = random.choice(alphabet)
    forth = random.choice(alphabet)
    fifth = random.randint(0, 9)
    alpha_id = str(first) + second.upper() + \
        third + forth.upper() + str(fifth)
    return alpha_id


def generate_n_id(n):
    """ And checks whether generated id is unique """
    temp_storage = []
    meta_storage = open("meta.json", encoding="utf-8")
    meta_storage = json.load(meta_storage)
    while len(temp_storage) < n:
        final_id = generate_id()
        response = requests.get(
            'https://www.renovationmap.org/building/' + final_id)
        if final_id not in temp_storage and final_id not in meta_storage.values() and response.status_code != 200:
            temp_storage.append(final_id)
    return temp_storage


def korpus_adder(adresses):
    """ Add 'корпус' and it`s serial number if there are the same addresses in a row"""
    temp = []
    n = 0
    m = 1

    for adress in adresses:
        if adresses[n] == adresses[n - 1]:
            temp.append(adresses[n])
            if n > 0:
                temp[n] = temp[n] + " / корпус " + str(m+1)
            if m == 1 and n != 0:
                temp[n - m] = temp[n - m] + " / корпус 1"
            m += 1
        else:
            m = 1
            temp.append(adress)
        n += 1
    return temp


def form_list_adresses(file1):
    adresses = open(f"cities/{file1}", "r",
                    encoding='utf-8').readlines()
    final_adresses = [i.replace('\n', '') for i in adresses]
    final_adresses = korpus_adder(final_adresses)
    return final_adresses


def create_json(output_result, file1):
    with open(f"output/{file1}_sample.json", "w", encoding="utf-8") as output:
        json.dump(output_result, output, ensure_ascii=False)
    with open("meta.json", "r+", encoding="utf-8") as output:
        data = json.load(output)
        data.update(output_result)
        output.seek(0)
        json.dump(data, output, ensure_ascii=False)


def create_names(final_adresses, final_storage):
    sum_list = [a + "_" + b for a,
                b in zip(final_adresses, final_storage)]
    sum_list = tuple(sum_list)
    return sum_list


def general_func(count):
    """ Combining addresses and their unique id """
    file1 = sys.argv[1]
    if file1.endswith('.txt'):
        final_storage = generate_n_id(count)
        final_adresses = form_list_adresses(file1)
        output_result = dict(zip(final_adresses, final_storage))
        create_json(output_result, file1)
        sum_list = create_names(final_adresses, final_storage)
        return sum_list
    else:
        print(
            'Extension of a file is incorrect.\nPlease use file, which extension is ".json" or ".txt"')
        sys.exit()


def creating_foldername():
    """ Function that creates name of rootfolder """

    # defining 'n' for all id_creation functions and calling them
    count = len(open(f"cities/{sys.argv[1]}", "r").readlines())
    final_name = general_func(count)
    return final_name


def create_spreadsheet_name(folder, service, main_id):
    a, b = folder.split('_', 1)
    spreadsheet_name = b+'_'+a+'_дослідження'
    file_metadata_spreadsheet = {
        'name': spreadsheet_name,
        'parents': [main_id]
    }
    service.files().copy(fileId=template_spreadsheet_id,
                         body=file_metadata_spreadsheet).execute()


def create_document_for_notes(service, main_id):
    document_name = 'Для нотування корисної інформації'
    body = {
        'name': document_name,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [main_id]
    }
    service.files().create(body=body).execute()


def create_folders():
    """ Func create folders due to needed folder tree"""
    rootfolders = creating_foldername()
    for folder in rootfolders:
        # pylint: disable=maybe-no-member
        main_id = create_folder_tree(folder)
        create_spreadsheet_name(folder, service, main_id)
        create_document_for_notes(service, main_id)
        time.sleep(1.0)


create_folders()
