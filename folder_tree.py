from personal_data import root_folder_id
from google_service import service


def create_file_metadata(folder_name, root_folder_id):
    metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [root_folder_id]
    }
    return metadata


def service_execute(metadata):
    # pylint: disable=maybe-no-member
    return service.files().create(body=metadata).execute(
    )


def create_folder_tree(folder):
    # pylint: disable=maybe-no-member
    file_metadata_main = create_file_metadata(folder, root_folder_id)
    main_folder = service_execute(file_metadata_main)
    main_id = main_folder.get('id')

    file_metadata_doc = create_file_metadata('documents', main_id)
    doc_folder = service_execute(file_metadata_doc)
    doc_id = doc_folder.get('id')

    file_metadata_image = create_file_metadata('images', main_id)
    image_folder = service_execute(file_metadata_image)
    image_id = image_folder.get('id')

    file_metadata_site = create_file_metadata('site', doc_id)
    service_execute(file_metadata_site)

    file_metadata_prochee = create_file_metadata('prochee', doc_id)
    service_execute(file_metadata_prochee)

    file_metadata_site = create_file_metadata('site', image_id)
    service_execute(file_metadata_site)

    file_metadata_prochee = create_file_metadata('prochee', image_id)
    service_execute(file_metadata_prochee)
    return main_id
