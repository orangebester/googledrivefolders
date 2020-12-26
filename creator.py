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


def creating_foldername():
    alphabet = list('abcdefghijklmnopqrstuvwxyz')

    def generate_id():
        """ Generates id each elements of which consist of random values """
        first = random.randint(0, 9)
        second = random.choice(alphabet)
        third = random.choice(alphabet)
        forth = random.choice(alphabet)
        fifth = random.randint(0, 9)
        not_final_id = str(first) + second.upper() + \
            third + forth.upper() + str(fifth)
        return not_final_id

    def generate_n_id(n):
        """ And checks whether generated id is unique """
        temp_storage = []
        while len(temp_storage) < n:
            final_id = generate_id()
            response = requests.get(
                'https://www.renovationmap.org/building/' + final_id)
            if final_id not in temp_storage and response.status_code != 200:
                temp_storage.append(final_id)
        return temp_storage

    def general_func(n):
        """ Combining addresses and their unique id """
        file1 = sys.argv[1]
        if file1.endswith('.txt'):
            # forming list of addreses and id`s
            final_storage = generate_n_id(n)
            adresses = open(f"cities/{file1}", "r",
                            encoding='utf-8').readlines()
            final_adresses = [i.replace('\n', '') for i in adresses]
            output_result = dict(zip(final_adresses, final_storage))
            # creating .json for storing addreses and id`s
            with open(f"output/{sys.argv[1]}_sample.json", "w", encoding="utf-8") as output:
                json.dump(output_result, output, ensure_ascii=False)
            with open("meta.json", "r+", encoding="utf-8") as output:
                data = json.load(output)
                data.update(output_result)
                output.seek(0)
                json.dump(data, output, ensure_ascii=False)
            # creating names for folders
            # python creator.py dnepr_testcopy.txt
            sum_list = [a + "_" + b for a,
                        b in zip(final_adresses, final_storage)]
            sum_list = tuple(sum_list)
            return sum_list
        else:
            print(
                'Extension of a file is incorrect.\nPlease use file, which extension is ".json" or ".txt"')
            sys.exit()

    # defining 'n' for all id_creation functions and calling them
    count = len(open(f"cities/{sys.argv[1]}", "r").readlines())
    final_name = general_func(count)
    return final_name


# creating folders due to our folder tree
rootfolders = creating_foldername()
root_folder_id = ['13owqZYtU3rQ60pm9wPgo-rrIrj_Ikxhn']

for folder in rootfolders:
    file_metadate = {
        'name': folder,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': root_folder_id
    }
    main_folder = service.files().create(body=file_metadate).execute()
    main_id = main_folder.get('id')

    file_metadate_doc = {
        'name': 'documents',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [main_id]
    }
    doc_folder = service.files().create(body=file_metadate_doc).execute()
    doc_id = doc_folder.get('id')

    file_metadate_image = {
        'name': 'images',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [main_id]
    }
    image_folder = service.files().create(body=file_metadate_image).execute()
    image_id = image_folder.get('id')

    file_metadate_site = {
        'name': 'site',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [doc_id]
    }
    service.files().create(body=file_metadate_site).execute()

    file_metadate_prochee = {
        'name': 'prochee',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [doc_id]
    }
    service.files().create(body=file_metadate_prochee).execute()

    file_metadate_site = {
        'name': 'site',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [image_id]
    }
    service.files().create(body=file_metadate_site).execute()

    file_metadate_prochee = {
        'name': 'prochee',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [image_id]
    }
    service.files().create(body=file_metadate_prochee).execute()
