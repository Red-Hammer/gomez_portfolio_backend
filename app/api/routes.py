from flask import url_for, request
from app.api import bp
from app.helpers import _construct_standard_response, _build_cors_preflight_response
from app.api.image_handling import allowed_file, write_image


@bp.route('/photos', methods=['GET'])
def photos():
    x = [
        {
            'src': "https://c2.staticflickr.com/9/8817/28973449265_07e3aa5d2e_b.jpg",
            'thumbnail': "https://c2.staticflickr.com/9/8817/28973449265_07e3aa5d2e_n.jpg",
            'thumbnailWidth': 320,
            'thumbnailHeight': 174,
            'caption': "After Rain (Jeshu John - designerspics.com)"
        },
        {
            "src": "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_b.jpg",
            "thumbnail": "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_n.jpg",
            "thumbnailWidth": 320,
            "thumbnailHeight": 212,
            "tags": [{"value": "Ocean", "title": "Ocean"}, {"value": "People", "title": "People"}],
            "caption": "Boats (Jeshu John - designerspics.com)"
        },

        {
            'src': "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_b.jpg",
            'thumbnail': "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_n.jpg",
            "thumbnailWidth": 320,
            "thumbnailHeight": 212
        },
        {
            'src': str(url_for('static', filename='images/Ramen_Eggesecute_smaller.png', _external=True)),
            # Need to host these on a CDN
            'thumbnail': str(url_for('static', filename='images/Ramen_Eggesecute_smaller.png', _external=True)),
            "thumbnailWidth": 320,
            "thumbnailHeight": 212
        }
    ]

    return _construct_standard_response(x)


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
            write_image(file)
            response = {'status': 'Success', 'message': 'The file was saved'}

            return _construct_standard_response(response)
