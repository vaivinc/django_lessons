from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem
from django.conf import settings


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

    match filter_name:
        case "price_increase":
            products = product.order_by("price")
        case "price_decrease":
            products = product.order_by("-price")
        case "rating_increase":
            products = product.order_by("rating")
        case "rating_decrease":
            products = product.order_by("-rating")

    return render(request, "index.html", context={"product": product, "categories": categories})


def about(request):
    return render(request, "about.html")


def products_details(request, product_id):
    products = get_object_or_404(Product, id=product_id)
    return render(request, "product_details.html", context={"product": products})


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get(settings.CART_SESSION_ID, {})

    if not request.user.is_authenticated():
        if cart.get(product_id):
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        request.session[settings.CART_SESSION_ID] = cart
    else:
        cart = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.amount += 1
            cart_item.save()
    return redirect("products:cart_detail")


def cart_detail(request):
    if not request.user.is_authenticated():
        cart = request.session.get(settings.CART_SESSION_ID, {})
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []
        total_price = 0
        for product in products:
            count = cart[str(product.id)]
            price = count * product.price
            total_price += price
            cart_items.append({"product": products, "count": count, "price": price})
        else:
            try:
                cart = request.user.cart
            except Cart.DoesNotExists:
                cart = None

            if not cart or not cart.items.count():
                cart_items = []
                total_price = 0
            else:
                cart_items = cart.items.select_related("product").all()
                total_price = sum(item.product.price * item.amount for item in cart_items)

        return render(request, "cart_detail.html", context={"cart_items": cart_items, "total_price": total_price})


def delete_item_cart(request, item_id):
    product = get_object_or_404(Product, id=item_id)

    if not request.user.is_authenticated():
        cart = request.session.get(settings.CART_SESSION_ID, {})
        if item_id in cart:
            del cart[item_id]
            request.session[settings.CART_SESSION_ID] = cart
        return redirect("products:cart_detail")
    else:
        try:
            cart = request.user.cart
            item_del = CartItem.objects.get(cart=cart, product=product)
            item_del.delete()
        except CartItem.DoesNotExist:
            cart = None
        return redirect("products:cart_detail")