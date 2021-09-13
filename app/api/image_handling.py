from werkzeug.utils import secure_filename
from pathlib import Path

from config import Config

# Create a db table for images.
# Have a function iterate through it and return a list of dicts to jsonify

# File Handling Stuff
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def write_image(file):
    safe_filename = secure_filename(file.filename)
    file.save(Path(Config.UPLOAD_FOLDER, safe_filename))


def write_file_metadata():
    pass
