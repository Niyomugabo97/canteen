from django.db import models
from django.contrib.auth.models import User

# ========================
# CATEGORY MODEL
# ========================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name


# ========================
# ITEM MODEL
# ========================
class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        """Return full image URL or placeholder if not available."""
        try:
            return self.image.url
        except:
            return '/static/img/placeholder.png'


# ========================
# ORDER MODEL
# ========================
class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("preparing", "Preparing"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

    def calculate_total(self):
        """Recalculate total price from related OrderItems."""
        total = sum(item.get_subtotal() for item in self.items.all())
        self.total_price = total
        self.save()
        return total


# ========================
# ORDER ITEM MODEL
# ========================
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def get_subtotal(self):
        """Return the total price for this order item."""
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"


# ========================
# PAYMENT MODEL
# ========================
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    method = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=10, default="RWF")
    status = models.CharField(max_length=12, default="pending")
    provider_payment_id = models.CharField(max_length=100, null=True, blank=True)
    provider_raw = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "payments"
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
