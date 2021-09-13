from app import db
from flask import url_for


class Image(db.Model):
    """Image location in the filesystem and relevant metadata"""
    id = db.Column(db.Integer, primary_key=True)
    upload_date = db.Column(db.DateTime, index=True)
    filename = db.Column(db.Unicode(255), index=True, unique=True)
    size = db.Column(db.Integer)
    name = db.Column(db.Unicode(255))
    caption = db.Column(db.Unicode(500))
    last_modified_date = db.Column(db.DateTime)


    def __repr__(self):
        return '<Image Metadata {}'.format(str(self.id) + ' ' + str(self.name) + ' '
                                           + str(self.size * 1000)
                                           )


    def api_to_dict(self):
        src = str(url_for('static', filename='images/' + self.filename))
        image_dict = {'src': src,
                      'thumbnail': src,
                      'thumbnailWidth': 320,
                      'thumbnailHeight': 212
                      }
        return image_dict
