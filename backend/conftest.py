import os
import django
import pytest
from rest_framework.test import APIClient

from django.contrib.auth.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "catalog.settings")
django.setup()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="1234"
    )


@pytest.fixture
def api_client():
    apiclient = APIClient()
    return apiclient


@pytest.fixture
def super_user():
    return User.objects.create_superuser(
        username="test_superuser",
        password="1234"
    )