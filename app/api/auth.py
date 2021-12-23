from app.models import Admin
from flask_login import login_user


def auth_user(username: str, password: str, remember: bool):
    user = Admin.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return False
    login_user(user, remember=remember)
    return True
