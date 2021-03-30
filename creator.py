import requests
import json
import sys
import random
from Google import Create_Service

CLIENT_SECRET_FILE = "client_secret.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# id of folder where you want to create other folders
root_folder_id = '1kg2bc_DNPVwu8sbHp9AC3hHjuJh4OCse'
# id of template spreadsheet that you need to copy
template_spreadsheet_id = '1Y6Rp4_kDz02wnqbkNq3ZwS5j88HQeFu26l0wNB5wtcY'


def generate_id():
    """ Generates id each elements of which consist of random values """
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
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


# creating folders due to our folder tree
rootfolders = creating_foldername()

for folder in rootfolders:
    # pylint: disable=maybe-no-member
    file_metadate = {
        'name': folder,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [root_folder_id]
    }
    main_folder = service.files().create(
        body=file_metadate).execute()
    main_id = main_folder.get('id')

    file_metadate_doc = {
        'name': 'documents',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [main_id]
    }
    doc_folder = service.files().create(
        body=file_metadate_doc).execute()
    doc_id = doc_folder.get('id')

    file_metadate_image = {
        'name': 'images',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [main_id]
    }
    image_folder = service.files().create(
        body=file_metadate_image).execute()
    image_id = image_folder.get('id')

    file_metadate_site = {
        'name': 'site',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [doc_id]
    }
    service.files().create(body=file_metadate_site).execute(
    )

    file_metadate_prochee = {
        'name': 'prochee',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [doc_id]
    }
    service.files().create(body=file_metadate_prochee).execute(
    )

    file_metadate_site = {
        'name': 'site',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [image_id]
    }
    service.files().create(body=file_metadate_site).execute(
    )

    file_metadate_prochee = {
        'name': 'prochee',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [image_id]
    }
    service.files().create(body=file_metadate_prochee).execute(
    )

    a, b = folder.split('_', 1)
    spreadsheet_name = b+'_'+a+'_дослідження'
    file_metadate_spreadsheet = {
        'name': spreadsheet_name,
        'parents': [main_id]
    }
    service.files().copy(fileId=template_spreadsheet_id,
                         body=file_metadate_spreadsheet).execute()
