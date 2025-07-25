import pytest

from products.models import Product, Category, Order, OrderItem, Cart, CartItem


@pytest.fixture
def product():
    category = Category.objects.create(name="test_category")

    product_ = Product.objects.create(
        name="test_product",
        category=category,
        nomenclature="test_nomenclature",
        price=100
    )

    return product_


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
def order(user, product):
    order_ = Order.objects.create(
        user=user,
        contact_name="test_contact_name",
        contact_email="test_contact_email",
        contact_phone="test_contact_phone",
        address="test_address"
    )

    OrderItem.objects.create(
        order=order_,
        product=product,
        price=100
    )

    OrderItem.objects.create(
        order=order_,
        product=product,
        amount=2,
        price=80
    )

    return order_


@pytest.fixture
def cart(user, product):
    cart_ = Cart.objects.create(
        user=user,
    )

    CartItem.objects.creaate(
        cart=cart_,
        product=product
    )

    CartItem.objects.creaate(
        cart=cart_,
        product=product,
        amount=2
    )

    return cart_