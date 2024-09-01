import os
from flask import current_app

def retrieve_name_extension(filestorage):
        filename = filestorage.filename
        name, extension = os.path.splitext(filename)
        return {"name": name, "extension": extension}

def get_full_path(relative_path):
    base_dir = current_app.config.get('MEDIA_BASE_DIR', '/absolute/path/to/media')

    # Construct the full path
    full_path = os.path.join(base_dir, relative_path.lstrip('/'))

    return full_path


