import pytest

from app.api.image_handling import allowed_file
from app import create_app
from config import Config

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


# Push the app context
@pytest.fixture
def client():
    app = create_app(TestConfig)
    # app_context = app.app_context()
    # app_context.push()
    return app


@pytest.mark.parametrize(
        'filename',
        [
            ('test.jpg'),
            ('test.png'),
            ('test.jpeg')

        ]
)
def test_allowed_file_success(filename):
    """Test that alowed_file returns True on valid file extensions"""
    # Arrange
    # parameterize arranges for us

    # Act
    actual = allowed_file(filename)

    # Assert
    assert actual is True


@pytest.mark.parametrize(
        'filename',
        [
            ('test.docx'),
            ('test.xlsx'),
            ('test.txt')

        ]
)
def test_allowed_file_failure(filename):
    """Test that allowed_file returns False when an invalid file extension is given"""
    actual = allowed_file(filename)
    assert actual is False
