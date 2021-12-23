import pytest
import os
import unittest
from flask import current_app
from app import db
from unittest.mock import MagicMock


from app import models
from app.api.image_handling import read_file_metadata


# I have no fucking idea how to mock the models out to test them
# Probably going to have to figure out a way to push an app context and not commit a session during testing.




#
# @pytest.fixture
# def mock_image_class(monkeypatch):
#     class MockedImageMeta(type):
#         static_instance = MagicMock(spec=models.Image)
#
#         def __getattr__(cls, key):
#             return MockedImageMeta.static_instance.__getattr__(key)
#
#     class MockImage(metaclass=MockedImageMeta):
#         original_cls = models.Image
#         instances = []
#
#         def __new__(cls, *args, **kwargs):
#             MockImage.instances.append(
#                     MagicMock(spec=MockImage.original_cls))
#             MockImage.instances[-1].__class__ = MockImage
#
#             return MockImage.instances[-1]
#
#     monkeypatch.setattr(models, 'Image', MockImage)
#
#
# # class
#
#
# @pytest.mark.parametrize(
#         'image_list,image_dict,expected',
#         [
#             (
#                     ['image'],
#                     {'src': 'source', 'metadata': 'yeet'},
#                     [{'src': 'source', 'metadata': 'yeet'}]
#             )
#         ]
# )
# def test_read_file_metadata_success(monkeypatch, mock_image_class, image_list, image_dict, expected):
#     """
#     Test that the output is what we expect under controlled conditions
#
#     If we're being honest, this function is mostly a wrapper around the app.models.Image.api_to_dict method.
#     That will be tested elsewhere.
#     """
#
#     mock_image_class.api_to_dict.return_value = image_dict
#     mock_image_class.query.all.return_value = image_list
#
#     # Arrange
#     # def fake_image_call(*args, **kwargs):
#     #     return image_list
#     #
#     #
#     # def fake_api_to_dict(*args, **kwargs):
#     #     return image_dict
#     #
#     #
#     # # need to add in some test data? or do better mocking.
#     # monkeypatch.setattr(models.Image.query, 'all', fake_image_call)
#     # monkeypatch.setattr(Image, 'api_to_dict', fake_api_to_dict)
#
#     # Act
#     actual = read_file_metadata()
#     print(actual)
#
#     # Assert
#     assert actual == expected
