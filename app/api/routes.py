from flask import url_for, request
from app.api import bp
from app.helpers import _construct_standard_response, _build_cors_preflight_response
from app.api.image_handling import allowed_file, write_image, write_file_metadata, read_file_metadata


@bp.route('/photos', methods=['GET', 'OPTIONS'])
def photos():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    if request.method == 'GET':
        images = read_file_metadata()
        return _construct_standard_response(images)


@bp.route('/uploadImage', methods=['POST', 'OPTIONS'])
def upload_image():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    if request.method == 'POST':
        if 'File' not in request.files:
            response = {'status': 'Failure', 'message': 'No file was attached to request'}
            return _construct_standard_response(response)

        file = request.files['File']

        if file.filename == '':
            response = response = {'status': 'Failure', 'message': 'The filename was blank'}
            return _construct_standard_response(response)

        # Move the file to a place
        if file and allowed_file(file.filename):
            image_size = write_image(file)

            write_file_metadata(file, image_size)

            response = {'status': 'Success', 'message': 'The file was saved'}

            return _construct_standard_response(response)
