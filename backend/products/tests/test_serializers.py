import pytest

from products.tests.fixtures import *
from products.serializers.product_serializer import ProductSerializer


@pytest.mark.django_db
def test_product_serializer_valid(category_fixture):
    data = {
        "name": "test_name",
        "description": "test_description",
        "stock": 3,
        "price": 100,
        "available": True,
        "category": category_fixture,
        "nomenclature": "test_nomenclature",
        "rating": 2,
        "discount": 10,
        "attributes": {}
    }

    serializer = ProductSerializer(data=data)

    assert serializer.is_valid()


@pytest.mark.django_db
def test_product_serializer_invalid(category_fixture):
    data = {
        "name": "*" * 101,
        "description": {},
        "stock": -3,
        "price": -100,
        "available": 55,
        "nomenclature": "*" * 101,
        "rating": "*",
        "discount": -10,
        "attributes": "*"
    }

    serializer = ProductSerializer(data=data)

    assert not serializer.is_valid()
    assert serializer.errors
    assert 'Ensure this field has no more than 100 characters.' in serializer.errors["name"]
    assert 'Must be a valid boolean.' in serializer.errors["available"]
    assert 'Ensure this field has no more than 50 characters.' in serializer.errors["nomenclature"]
    assert 'A valid number is required.' in serializer.errors["rating"]
    for field in data.keys():
        assert field in serializer.errors