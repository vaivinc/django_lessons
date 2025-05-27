from rest_framework import serializers
from ..models import Category


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UserSerializers(serializers.ModelSerializer):
    user = CategorySerializers(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"

