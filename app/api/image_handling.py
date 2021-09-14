from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
import os

from config import Config
from app.models import Image
from app import db

# Have a function iterate through it and return a list of dicts to jsonify

# File Handling Stuff
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def write_image(file):
    safe_filename = secure_filename(file.filename)
    file.save(Path(Config.UPLOAD_FOLDER, safe_filename))

    return os.stat(Path(Config.UPLOAD_FOLDER, safe_filename)).st_size


def write_file_metadata(data, image_size) -> None:
    image_meta = Image.query.filter_by(filename=data.filename).first()

    if image_meta is None:
        new_image = Image(
                upload_date=datetime.now(),
                filename=data.filename,
                size=image_size,
                name='.'.join(data.filename.split('.')[:-1]),
                caption='placeholder for now',
                last_modified_date=datetime.now()
        )
        db.session.add(new_image)
        db.session.commit()

    else:
        image_meta.size = image_size
        image_meta.caption = 'New Caption'
        image_meta.last_modified_date = datetime.now()
        db.session.commit()


def read_file_metadata() -> list:
    images = Image.query.all()
    output_list = []
    for i in images:
        output_list.append(i.api_to_dict())

    return output_list
