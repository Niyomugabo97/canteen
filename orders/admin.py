# orders/admin.py
from django.contrib import admin
from .models import Category, Item, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("price",)
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "created_at", "status", "total_price")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]

admin.site.register(Category)
admin.site.register(Item)

