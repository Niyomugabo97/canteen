# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Menu / Items
    path('', views.menu, name='menu-list'),
    path('menu/', views.menu, name='menu'),
    path('item/<int:item_id>/', views.item_detail, name='item-detail'),

    # Cart
    path('cart/', views.view_cart, name='cart'),
    path('cart/', views.view_cart, name='view-cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='cart-add'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='cart-remove'),

    # Orders
    path('orders/', views.view_orders, name='order-list'),
    path('orders/', views.view_orders, name='view-orders'),
    path('orders/place/', views.place_order, name='place-order'),
    path('orders/success/<int:order_id>/', views.order_success, name='order-success'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel-order'),

    # Accounts
    path('accounts/signup/', views.register_user, name='signup-view'),
    path('accounts/login/', views.login_user, name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
# ========================
# Admin Dashboard Routes
# ========================
path('dashboard/', views.dashboard_home, name='dashboard-home'),  # Main admin dashboard
path('dashboard/orders/', views.order_dashboard, name='order-dashboard'),  # All orders
path('dashboard/item/add/', views.add_item, name='add-item'),
path('dashboard/item/edit/<int:item_id>/', views.edit_item, name='edit-item'),
path('dashboard/item/delete/<int:item_id>/', views.delete_item, name='delete-item'),

# Manage Admins
path('dashboard/manage-users/', views.manage_users, name='manage-users'),
path('dashboard/make-admin/<int:user_id>/', views.make_admin, name='make-admin'),

path('dashboard/make-superuser/<int:user_id>/', views.make_superuser, name='make-superuser'),

# Manage Orders
path('dashboard/manage-orders/', views.manage_orders, name='manage-orders'),
path('dashboard/update-order/<int:order_id>/', views.update_order, name='update-order'),
path('dashboard/delete-order/<int:order_id>/', views.delete_order, name='delete-order'),


]
