import os

def retrieve_name_extension(filestorage):
        filename = filestorage.filename
        name, extension = os.path.splitext(filename)
        return {"name": name, "extension": extension}

