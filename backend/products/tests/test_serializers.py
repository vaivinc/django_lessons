import pytest

from products.tests.fixtures import category_fixture, product_discount, product, order
from products.serializers.product_serializer import ProductSerializer
from products.serializers.order_serializer import OrderSerializer, OrderItemSerializer
from products.models import OrderItem


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


@pytest.mark.django_db
def test_product_serializer_read_only(category_fixture):
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
    assert "category" not in serializer.data


@pytest.mark.django_db
def test_product_serializer_method_field(product_discount):
    serializer = ProductSerializer(product_discount)

    assert serializer.data["discount_price"] == product_discount.discount_price
    assert serializer.data["discount_price"] == 80


@pytest.mark.django_db
def test_order_serializer_read_only(user, order):
    data = {
        "user": user.id,
        "contact_name": "test-name",
        "contact_email": "testemail@gmail.com",
        "contact_phone": "385943107401",
        "address": "test-address"
    }
    serializer = OrderSerializer(data=data)

    assert serializer.is_valid()
    assert "items" not in serializer.validated_data

    serializer = OrderSerializer(order)

    assert "items" in serializer.data


@pytest.mark.django_db
def test_order_serializer_items(user, order):

    serializer = OrderSerializer(order)
    items = serializer.data["items"]

    assert len(items) == 2



