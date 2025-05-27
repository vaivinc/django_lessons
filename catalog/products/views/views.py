from PIL.Image import item
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, redirect

from ..forms import OrderCreateForm
from ..models import Product, Category, OrderItem, Payment, CartItem, Cart
from django.conf import settings


def calculate_discount(value, arg):
    discount_value = value * arg / 100
    return value - discount_value


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
    if not request.user.is_authenticated():
        cart = request.session.get(settings.CART_SESSION_ID, {})
        if cart.get(product_id):
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        request.session[settings.CART_SESSION_ID] = cart
    else:
        cart = request.user.cart
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


def checkout(request):
    if (request.user.is_authenticated() and not getattr(request.user, "cart", None)) or (not request.user.
        is_authenticated and not request.session.get(settings.CART_SESSION_ID)):
        messages.error(request, "Cart is empty")
        return redirect("products:cart_detail")

    if request.method == "GET":
        form = OrderCreateForm()
        if request.user.is_authenticated():
            form.initial["contact_email"] = request.user.email
    elif request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            if request.user.is_authenticated:
                cart = getattr(request.user, "cart")
                cart_items = cart.items.select_related("product").all()
            else:
                cart = request.session.get(settings.CART_SESSION_ID)
                cart_items = []
                for product_id, amount in cart.items():
                    product = Product.objects.get(id=product_id)
            cart_items.append({"product": product, "amount": amount})

            items = OrderItem.objects.bulk_create(
                [OrderItem(order=order,
                           product=item.product,
                           amount=item.amount,
                           price=calculate_discount(item.product.price, item.product)
                           )
                 for item in cart_items
                 ]
             )

            total_price = sum(item.product.price * item.amount for item in items)
            method = form.cleaned_data.get("payment_method")
            if method != "cash":
                Payment.objects.create(order=order, provider=method, amount=total_price)
            else:
                order.status = 2

            order.save()

    return render(request, "checkout.html", context={"form": form})