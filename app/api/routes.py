from flask import request, redirect, url_for, flash, render_template
from app.api import bp
from app.helpers import _construct_standard_response, _build_cors_preflight_response
from app.api.image_handling import allowed_file, write_image, write_file_metadata, read_file_metadata
from flask_login import current_user, logout_user, login_required
from app.api.forms import LoginForm, FileUpload
from app.api.auth import auth_user


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


@bp.route('/auth', methods=['POST', 'GET'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('api.admin'))

    form = LoginForm()

    if form.validate_on_submit():
        if not auth_user(form.username.data, form.password.data, form.remember_me.data):
            flash('Invalid Username or Password')
            return redirect(url_for('api.auth'))

        return redirect(url_for('api.admin'))

    return render_template(
            'login.html',
            title='Sign In',
            form=form
    )


@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    form = FileUpload()

    if form.validate_on_submit():
        file = form.file.data
        homepage_ind = form.is_homepage.data

        if file and allowed_file(file.filename):
            image_size, safe_filename = write_image(file)

            write_file_metadata(file, image_size, homepage_ind, safe_filename)

            return redirect(url_for('api.admin'))

        else:
            flash('This filetype is not allowed')
            return redirect(url_for('main.home'))

    return render_template(
            'image-upload.html',
            title='Admin',
            form=form
    )


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('api.auth'))
