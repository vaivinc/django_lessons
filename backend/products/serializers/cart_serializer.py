from rest_framework import serializers

from .product_serializer import ProductSerializer
from ..models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'item_total', 'amount']

        def get_item_total(self, obj):
            return obj.item_total

        def validate_amount(self, value):
            if value <= 0:
                raise serializers.ValidationError("The price should be higher than 0")
            else:
                return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source="items", many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['user', 'created_at', 'items', 'total']

        def get_total(self, obj):
            return sum([item.item_total for item in obj.items.all()])