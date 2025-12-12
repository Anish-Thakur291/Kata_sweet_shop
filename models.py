from django.db import models
from django.contrib.auth.models import User


class Sweet(models.Model):
    CATEGORY_CHOICES = [
        ('chocolate', 'Chocolate'),
        ('candy', 'Candy'),
        ('pastry', 'Pastry'),
        ('ice_cream', 'Ice Cream'),
        ('cake', 'Cake'),
        ('cookie', 'Cookie'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
