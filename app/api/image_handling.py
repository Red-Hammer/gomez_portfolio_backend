from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
import os


from config import Config
from app.models import Image
from app import db


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def allowed_file(filename: str):
    """
    checks to make sure the filename contains a valid extension
    :param filename: filename to check
    :return: bool
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def write_image(file):
    """
    Saves an image file stream to
    :param file:
    :return:
    """
    safe_filename = secure_filename(file.filename)
    file.save(Path(Config.UPLOAD_FOLDER, safe_filename))

    return os.stat(Path(Config.UPLOAD_FOLDER, safe_filename)).st_size, safe_filename


def write_file_metadata(data, image_size: int, homepage_ind: bool, safe_filename: str) -> None:
    image_meta = Image.query.filter_by(filename=data.filename).first()

    if image_meta is None:
        new_image = Image(
                upload_date=datetime.now(),
                filename=safe_filename,
                size=image_size,
                name='.'.join(data.filename.split('.')[:-1]),
                caption='placeholder for now',
                last_modified_date=datetime.now(),
                homepage_ind=homepage_ind
        )
        db.session.add(new_image)
        db.session.commit()

    else:
        image_meta.size = image_size
        image_meta.caption = 'New Caption'
        image_meta.last_modified_date = datetime.now()
        image_meta.homepage_ind = homepage_ind
        db.session.commit()


def read_file_metadata(homepage: bool = False) -> list:
    output_list = []

    if not homepage:
        images = Image.query.all()
    else:
        images = Image.query.filter_by(homepage_ind=1).all()

    for i in images:
        output_list.append(i.api_to_dict())

    return output_list
