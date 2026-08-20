import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(username="anna", email="anna@example.com", password="strong-pass-123")
