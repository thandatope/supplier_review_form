from flask import current_app
import shutil
import os
import datetime

def generate_datapack_attachment(company):
    zipfile_to_create = current_app.config.get("UPLOADED_ZIPFILES_DEST") + f"/{company}"
    root_folder = current_app.config.get("UPLOADED_DATAPACKFILES_DEST")
    zip_path = shutil.make_archive(zipfile_to_create, 'zip', root_folder, company)
    os.rmdir(root_folder + f"/{company}")
    return zip_path