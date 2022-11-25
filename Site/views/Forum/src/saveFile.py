import os
import PIL

from flask import current_app

from Site import app
from Site.views.Forum.src.utilis import generate_random_string


UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]
SIZE = 500, 500

def saveFile(form):
    filename = "{}-{}".format(generate_random_string(), form.filename)
    path = os.path.join(current_app.root_path, UPLOAD_FOLDER, filename)
    
    img = PIL.Image.open(form)
    img.thumbnail(SIZE, PIL.Image.ANTIALIAS)
    img.save(path)

    return filename