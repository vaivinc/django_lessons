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

    class Meta:
        ordering = ['-created_at']
        db_table = 'products'
        unique_together = ['name', 'nomenclature']

    def __str__(self):
        return f"{self.name} ({self.nomenclature})"