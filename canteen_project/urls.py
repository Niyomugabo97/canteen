from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from orders import views as order_views  # import your custom admin dashboard views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom admin dashboard for managing items/categories
    path('dashboard/', order_views.dashboard_home, name='dashboard-home'),
    path('dashboard/item/add/', order_views.add_item, name='add-item'),
    path('dashboard/item/edit/<int:item_id>/', order_views.edit_item, name='edit-item'),
    path('dashboard/item/delete/<int:item_id>/', order_views.delete_item, name='delete-item'),

    # Orders app routes (user side: menu, cart, etc.)
    path('', include('orders.urls')),
]

# Serve uploaded images during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
