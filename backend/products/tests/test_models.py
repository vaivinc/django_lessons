import pytest

from products.models import Product, Category, Cart, CartItem, Order, OrderItem
from products.tests.fixtures import product, product_discount, order

@pytest.mark.django_db
def test_product_model():
    category = Category.objects.create(name="test_category")
    product = Product.objects.create(name="test_product",
                                     category=category,
                                     nomenclature="test_nomenclature",
                                     price=100,
                                     discount=10)

    assert product.discount_price == 90
    assert product.category.name == "test_category"


@pytest.mark.django_db
def test_cart_model_one_product(user, product):
    cart_item = CartItem.objects.create(cart=user.cart,
                                        product=product)

    assert cart_item.item_total == product.price
    assert user.cart.total == product.price


@pytest.mark.django_db
def test_cart_model_multiple_products(user, product):
    cart_item = CartItem.objects.create(cart=user.cart,
                                        product=product,
                                        amount=10)

    assert cart_item.item_total == product.price * 10
    assert user.cart.total == product.price * 10


@pytest.mark.django_db
def test_cart_model_discount_product(user, product_discount):
    cart_item = CartItem.objects.create(cart=user.cart,
                                        product=product_discount,
                                        )

    assert cart_item.item_total == 80
    assert user.cart.total == 80


@pytest.mark.django_db
def test_cart_model_different_products(user, product_discount, product):
    cart_item = CartItem.objects.create(cart=user.cart,
                                        product=product_discount,
                                        )

    cart_item_2 = CartItem.objects.create(cart=user.cart,
                                          product=product,
                                        )

    assert user.cart.total == 180


# @pytest.mark.django_db
# def test_order_model(user):
#     data = Order.objects.create(
#         user=user,
#         contact_name="test_contact_name",
#         contact_email="test_contact_email",
#         contact_phone="test_contact_phone",
#         address="test_address"
#     )
#
#     OrderItem.objects.create(
#         order=order,
#         product=product,
#         price=100
#     )
#
#     OrderItem.objects.create(
#         order=order,
#         product=product,
#         amount=2,
#         price=80
#     )
#
#     assert data.contact_name == "test_contact_name"
#     assert data.address == "test_address"


