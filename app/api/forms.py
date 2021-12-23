from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class FileUpload(FlaskForm):
    file = FileField('Image', validators=[FileRequired()])
    is_homepage = BooleanField('Put this on the Homepage?', default=False)
    submit = SubmitField('Upload')
