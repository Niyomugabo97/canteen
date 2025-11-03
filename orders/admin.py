# orders/admin.py
from django.contrib import admin
from .models import Category, Item, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ("item", "quantity", "price")
    readonly_fields = ("price",)
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "phone",
        "address",
        "created_at",
        "status",
        "total_price",
        "items_summary",
    )
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "phone", "address", "user__username")
    inlines = [OrderItemInline]

    def items_summary(self, obj):
        items = obj.items.select_related("item").all()
        parts = []
        for oi in items:
            item_name = oi.item.name if oi.item else "(deleted item)"
            parts.append(f"{item_name} x{oi.quantity}")
        return ", ".join(parts)
    items_summary.short_description = "Items"

admin.site.register(Category)
admin.site.register(Item)

