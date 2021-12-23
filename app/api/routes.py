from flask import request, redirect, url_for, flash, render_template
from app.api import bp
from app.helpers import _construct_standard_response, _build_cors_preflight_response
from app.api.image_handling import allowed_file, write_image, write_file_metadata, read_file_metadata
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin
from app.api.forms import LoginForm


@bp.route('/gallery-photos', methods=['GET', 'OPTIONS'])
def gallery_photos():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    if request.method == 'GET':
        images = read_file_metadata()
        return _construct_standard_response(images)


@bp.route('/home-photos', methods=['GET', 'OPTIONS'])
def home_photos():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    if request.method == 'GET':
        images = read_file_metadata(homepage=True)
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
        homepage_ind = request.form['isHomepage']

        if homepage_ind == 'true':
            homepage_ind = True
        else:
            homepage_ind = False

        if file.filename == '':
            response = {'status': 'Failure', 'message': 'The filename was blank'}
            return _construct_standard_response(response)

        # Move the file to a place
        if file and allowed_file(file.filename):
            image_size, safe_filename = write_image(file)

            write_file_metadata(file, image_size, homepage_ind, safe_filename)

            response = {'status': 'Success', 'message': 'The file was saved'}

            return _construct_standard_response(response)


@bp.route('/auth', methods=['POST', 'GET'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('api.admin'))

    form = LoginForm()

    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('api.auth'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('api.admin'))

    return render_template(
            'login.html',
            title='Sign In',
            form=form
    )


@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file attached')
            return redirect(url_for('api.admin'))

        file = request.files['file']
        homepage_ind = request.form['isHomepage']

        if homepage_ind == 'true':
            homepage_ind = True
        else:
            homepage_ind = False

        if file.filename == '':
            flash('Filename is blank')

        # Move the file to a place
        if file and allowed_file(file.filename):
            image_size, safe_filename = write_image(file)

            write_file_metadata(file, image_size, homepage_ind, safe_filename)

            return redirect(url_for('api.admin'))

    return '''  <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=checkbox name=isHomepage>
      <input type=submit value=Upload>
    </form>'''


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('api.auth'))
