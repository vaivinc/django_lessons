import uuid

import pytest
from django.urls import reverse
from django.contrib.auth.models import User


from .fixtures import *
from products.models import Product


@pytest.mark.django_db
def test_products_list_empty(api_client):
    url = reverse("products:products-list")

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_products_list(api_client, product, product_discount):
    url = reverse("products:products-list")

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_products_detail(api_client, product):
    url = reverse("products:products-detail", kwargs={"pk": product.id})

    response = api_client.get(url)

    assert response.status_code == 200
    assert product.name == response.data["name"]


@pytest.mark.django_db
def test_products_detail_not_found(api_client, product):
    url = reverse("products:products-detail", kwargs={"pk": 124665})

    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_products_update(api_client, product):
    url = reverse("products:products-detail", kwargs={"pk": product.id})

    response = api_client.patch(url, data={"price": 1573})

    assert response.status_code == 403


@pytest.mark.django_db
def test_products_update_not_authorized(api_client, product):
    url = reverse("products:products-detail", kwargs={"pk": product.id})

    response = api_client.patch(url, data={"price": 1573})

    assert response.status_code == 403


@pytest.mark.django_db
def test_products_update(api_client, product, super_user):

    url = reverse("products:products-detail", kwargs={"pk": product.id})
    api_client.force_authenticate(super_user)

    response = api_client.patch(url, data={"price": 1573})

    assert response.status_code == 200
    assert response.data.get("price") == 1573
    assert product.price == 1573


@pytest.mark.django_db
def test_products_create(api_client, product, category_fixture, super_user):
    url = reverse("products:products-list")

    data = {
        "name": "test_name",
        "description": "test_description",
        "category": category_fixture.id,
        "nomenclature": str(uuid.uuid4()),
    }

    api_client.force_authenticate(super_user)

    response = api_client.post(url, data=data)

    assert response.status_code == 201
    assert response.data.get("name") == "test_name"
