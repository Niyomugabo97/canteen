# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Menu / Items
    path('', views.menu, name='menu-list'),            # keep old name for templates
    path('menu/', views.menu, name='menu'),            # name used in redirects
    path('item/<int:item_id>/', views.item_detail, name='item-detail'),

    # Cart
    path('cart/', views.view_cart, name='cart'),       # keep old name for navbar
    path('cart/', views.view_cart, name='view-cart'),  # name used in redirects
    path('cart/add/<int:item_id>/', views.add_to_cart, name='cart-add'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='cart-remove'),

    # Orders
    path('orders/', views.view_orders, name='order-list'),   # keep old name for templates
    path('orders/', views.view_orders, name='view-orders'),  # convenience name
    path('orders/place/', views.place_order, name='place-order'),
    path('orders/success/<int:order_id>/', views.order_success, name='order-success'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel-order'),

    # Accounts
    path('accounts/signup/', views.register_user, name='signup-view'),
    path('accounts/login/', views.login_user, name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),

    # Custom Admin Dashboard Routes
    path('dashboard/', views.dashboard_home, name='dashboard-home'),
    path('dashboard/item/add/', views.add_item, name='add-item'),
    path('dashboard/item/edit/<int:item_id>/', views.edit_item, name='edit-item'),
    path('dashboard/item/delete/<int:item_id>/', views.delete_item, name='delete-item'),
]
