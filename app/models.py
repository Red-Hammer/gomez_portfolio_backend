from app import db
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class Image(db.Model):
    """Image location in the filesystem and relevant metadata"""
    id = db.Column(db.Integer, primary_key=True)
    upload_date = db.Column(db.DateTime, index=True)
    filename = db.Column(db.Unicode(255), index=True, unique=True)
    size = db.Column(db.Integer)
    name = db.Column(db.Unicode(255))
    caption = db.Column(db.Unicode(500))
    last_modified_date = db.Column(db.DateTime)
    homepage_ind = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<Image Metadata {}'.format(str(self.id) + ' ' + str(self.name) + ' '
                                           + str(self.size / 1000) + ' Filename:' + str(self.filename)
                                           )


    def api_to_dict(self):
        src = str(url_for('static', filename='images/' + self.filename, _external=True))
        image_dict = {'src': src,
                      'thumbnail': src,
                      'thumbnailWidth': 320,
                      'thumbnailHeight': 212
                      }
        return image_dict


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(500))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))
