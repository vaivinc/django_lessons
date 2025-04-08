from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def index(request):
    product = Product.objects.all()
    categories = Category.objects.all()

    category_name = request.GET.get("category")
    filter_name = request.GET.get("filter")
    product_name = request.GET.get("search")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if product_name:
        product = product.filter(name__icontains=product_name)

    if category_name:
        category = Category.objects.get(name=category_name)
        product = product.filter(category=category)

    if min_price:
        product = product.filter(price__gte=min_price)

    if max_price:
        product = product.filter(price__lte=max_price)

    if filter_name == "price_increase":
        product = product.order_by("price")
    elif filter_name == "price_decrease":
        product = product.order_by("-price")
    elif filter_name == "rating_increase":
        product = product.order_by("rating")
    elif filter_name == "rating_decrease":
        product = product.order_by("-rating")
    else:
        ...

    return render(request, "index.html", context={"product": product, "categories": categories})


def about(request):
    return render(request, "about.html")


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_details.html", context={"product": product})