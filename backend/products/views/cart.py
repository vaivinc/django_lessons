from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from products.models import Cart, CartItem, Product, OrderItem, Payment, Order
from products.serializers.cart_serializer import CartItemSerializer, CartSerializer
from products.serializers.product_serializer import ProductSerializer
from utils.email import send_order_confirmation_email
from products.forms import OrderCreateForm


class CartViewSet(ViewSet):
    @action(detail=False, methods=["post"], url_path="add-product")
    def add(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart = request.user.cart
            cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
            if created:
                cart_item.amount = 1
            else:
                cart_item.amount += 1
            cart_item.save()
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default={})
            cart[str(product_id)] = cart.get(str(product_id), default=0) + 1
        return Response({"message": f"Product with id {product_id} added"}, status=200)

    @action(detail=False, methods=["get"], url_path="get-cart-items")
    def items(self, request):
        if request.user.is_authenticated:
            cart = request.user.cart
            cart.items.select_related("product").all()
            data = request.user.cart
            return Response(CartItemSerializer(cart).data)
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default={})
            products = Product.objects.filter(id__in=cart.keys())

            items = []
            total = 0
            for product in products:
                data = ProductSerializer(product). data
                amount = cart.get(product.id)
                item_total = (product.discount_price or product.price) * amount
                items.append({
                    "product": product,
                    "amount": amount,
                    "item_total": item_total,
                    "cart": None
                })
                total += item_total
            return Response({"user": request.user, "created_at": None})

    @action(detail=False, methods=["post"], url_path="cart-checkout")
    def checkout(self, request):
        if request.user.is_authenticated:
            cart = request.user.cart
            if not cart or cart.items.count() == 0:
                return Response({"error": "Cart is empty"}, status=400)

        else:
            if not request.session.get(settings.CART_SESSION_ID, default={}):
                return Response({"error": "Cart is empty"}, status=400)

        form = OrderCreateForm(request.data)
        if not form.is_valid():
            return Response({"errors": form.errors}, status=400)
        order = form.save(commit=False)

        if request.user.is_authenticated:
            order.user = request.user

        order.save()

        if request.user.is_authenticated:
            cart_items = order.user.cart.items.select_related("product").all()
            items = OrderItem.objects.bulk_create([OrderItem(order=order,
                                                             product=item.product,
                                                             amount=item.amount,
                                                             price=item.discount_price or item.price)
                                                             for item in cart_items]
                                                             )

        else:
            cart_items = order.user.cart.items.select_related("product").all()
            items = OrderItem.objects.bulk_create([OrderItem(order=order,
                                                             product=item["product"],
                                                             amount=item.amount["amount"],
                                                             price=item["product"] or item["product"])
                                                             for item in cart_items]
                                                             )

        method = form.cleaned_data["payment_method"]
        total = sum(item.item_total for item in items)
        if method != "cash":
            Payment.objects.create(order=order, provider=method, amount=total)
        else:
            order.status = Order.Status.PROCESSING
            order.save()

        if request.user.is_authenticated:
            request.user.cart.items.all().delete()

        else:
            cart.clear()

        send_order_confirmation_email(order=order)

        return Response({"message": f" Order {order.id} is created"}, status=200)