from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.menu_list, name='menu-list'),
    path('item/<int:pk>/', views.item_detail, name='item-detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:item_id>/', views.cart_add, name='cart-add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart-remove'),
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel-order'),
    path('accounts/signup/', views.signup_view, name='signup-view'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
]
