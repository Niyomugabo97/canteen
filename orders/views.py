from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Order, OrderItem
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import login, logout, authenticate

# ============================
# MENU + CART + CHECKOUT
# ============================

def menu_list(request):
    items = Item.objects.filter(available=True).order_by("category", "name")
    return render(request, "orders/menu_list.html", {"items": items})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, "orders/item_detail.html", {"item": item})

# Cart helper
def _get_cart(request):
    return request.session.setdefault("cart", {})

def cart_view(request):
    cart = _get_cart(request)
    cart_items = []
    total = 0
    for item_id_str, qty in cart.items():
        try:
            item = Item.objects.get(pk=int(item_id_str))
        except Item.DoesNotExist:
            continue
        subtotal = item.price * qty
        total += subtotal
        cart_items.append({"item": item, "quantity": qty, "subtotal": subtotal})
    return render(request, "orders/cart.html", {"cart_items": cart_items, "total": total})

def cart_add(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(Item, pk=item_id)
    qty = int(request.POST.get("quantity", 1)) if request.method == "POST" else 1
    key = str(item_id)
    cart[key] = cart.get(key, 0) + qty
    request.session.modified = True
    messages.success(request, f"Added {qty} x {item.name} to cart.")
    return redirect("orders:menu-list")

def cart_remove(request, item_id):
    cart = _get_cart(request)
    key = str(item_id)
    if key in cart:
        del cart[key]
        request.session.modified = True
        messages.success(request, "Removed item from cart.")
    return redirect("orders:cart")

# ============================
# ORDERS
# ============================

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "orders/order_detail.html", {"order": order})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if order.status in ['pending', 'preparing']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, f"Order #{order.id} has been cancelled.")
    else:
        messages.error(request, "This order cannot be cancelled.")
    return redirect('orders:order-list')

# ============================
# AUTHENTICATION
# ============================

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('orders:menu-list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Authenticate using username, find by email
            try:
                from django.contrib.auth.models import User
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
                return render(request, 'registration/login.html', {'form': form})
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "You've been logged in!")
                return redirect('orders:menu-list')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You’ve been logged out.")
    return redirect("orders:login")



@login_required
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect("orders:menu-list")

    cart_items = []
    total = 0
    for item_id_str, qty in cart.items():
        item = get_object_or_404(Item, pk=int(item_id_str))
        subtotal = item.price * qty
        total += subtotal
        cart_items.append({"item": item, "quantity": qty, "subtotal": subtotal})

    if request.method == "POST":
        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=request.user.username,
            phone="N/A",
            address="N/A",
            total_price=total,
        )
        for c in cart_items:
            OrderItem.objects.create(
                order=order,
                item=c["item"],
                quantity=c["quantity"],
                price=c["item"].price,
            )
        # Clear cart
        request.session["cart"] = {}
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect("orders:order-list")

    return render(request, "orders/checkout.html", {"cart_items": cart_items, "total": total})
