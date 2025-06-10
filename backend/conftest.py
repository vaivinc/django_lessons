import os
import django
import pytest
from django.contrib.auth.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()


@pytest.fixture()
def user():
    return User.objects.create_user(
        username="testuser",
        password="1234"
    )