import pytest

from products.models import Product, Category, Order, OrderItem


@pytest.fixture
def product():
    category = Category.objects.create(name="test_category")

    return Product.objects.create(
        name="test_product",
        category=category,
        nomenclature="test_nomenclature",
        price=100
    )


@pytest.fixture
def category_fixture():
    return Category.objects.create(name="category_fixture")


@pytest.fixture
def product_discount():
    category = Category.objects.create(name="test_category")

    return Product.objects.create(
        name="test_product_2",
        category=category,
        nomenclature="test_nomenclature_2",
        price=100,
        discount=20
    )


@pytest.fixture
def order():
    return Order.objects.create(
        contact_name="test_contact_name",
        contact_email="test_contact_email",
        contact_phone="test_contact_phone",
        address="test_address"
    )

