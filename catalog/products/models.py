from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    available = models.BooleanField(default=True)
    nomenclature = models.CharField(unique=True, max_length=50)
    image_path = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0.0)
    attributes = models.JSONField(default=dict, null=True)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)

    @property
    def discount_price(self):
        if self.discount:
            return round(self.price - (self.price * self.discount / 100), 2)

    class Meta:
        ordering = ['-created_at']
        db_table = 'products'
        unique_together = ['name', 'nomenclature']

    def __str__(self):
        return self.name, self.nomenclature


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}\"s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    @property
    def item_total(self):
        return self.product.price * self.amount if not self.product.discount else self.product.price * self.amount


    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.name} : {self.amount}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="orders")
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Status(models.IntegerChoices):
        NEW = 1
        PROCESSING = 2
        SHIPPED = 3
        COMPLETED = 4
        CANCELED = 5

    status = models.IntegerField(choices=Status, default=Status.NEW)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.id} : {self.product.name} : {self.amount} : ${self.price}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    provider = models.CharField(max_length=20,
                                choices={"liqpay": "LiqPay",
                                         "monopay": "MonoPay",
                                         "googlepay": "Google Pay"
                                         })
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Status(models.IntegerChoices):
        PENDING = 1
        PAID = 2
        FAILED = 3
    status = models.IntegerField(choices=Status, default=Status.PENDING)
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

