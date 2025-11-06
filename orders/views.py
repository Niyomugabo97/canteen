from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Item, Category, Order
from .forms import ItemForm, LoginForm, OrderForm, CustomUserCreationForm
from django.contrib.admin.views.decorators import staff_member_required

from .models import Order, Item


# ============================
# MENU & CATEGORY DISPLAY
# ============================

def menu(request):
    categories = Category.objects.all()
    items = Item.objects.all()
    query = request.GET.get('q')
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'orders/menu_list.html', {'categories': categories, 'items': items})


def category_items(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = Item.objects.filter(category=category)
    return render(request, 'orders/category_items.html', {'category': category, 'items': items})


def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'orders/item_detail.html', {'item': item})


# ============================
# CART FUNCTIONALITY (session-based)
# ============================

def _get_cart(request):
    return request.session.setdefault('cart', {})


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = _get_cart(request)
    key = str(item_id)
    cart[key] = cart.get(key, 0) + 1
    request.session.modified = True
    messages.success(request, f"{item.name} added to your cart.")
    return redirect('orders:menu')


@login_required
def view_cart(request):
    cart = _get_cart(request)
    cart_items = []
    total_price = 0
    for item_id_str, qty in cart.items():
        try:
            product = Item.objects.get(pk=int(item_id_str))
        except Item.DoesNotExist:
            continue
        subtotal = product.price * qty
        total_price += subtotal
        cart_items.append({'item': product, 'quantity': qty, 'subtotal': subtotal})
    return render(request, 'orders/cart.html', {'cart_items': cart_items, 'total': total_price})


@login_required
def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    key = str(item_id)
    if key in cart:
        del cart[key]
        request.session.modified = True
        messages.success(request, "Item removed from your cart.")
    return redirect('orders:view-cart')


# ============================
# ORDER FUNCTIONALITY
# ============================

@login_required
def place_order(request):
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('orders:menu')

    order = Order.objects.create(user=request.user, full_name=request.user.username, phone='N/A', address='N/A')

    total = 0
    from .models import OrderItem
    for item_id_str, qty in cart.items():
        try:
            product = Item.objects.get(pk=int(item_id_str))
        except Item.DoesNotExist:
            continue
        total += product.price * qty
        OrderItem.objects.create(order=order, item=product, quantity=qty, price=product.price)

    order.total_price = total
    order.save()
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, "Order placed successfully!")
    return redirect('orders:view-orders')


@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def cancel_order(request, order_id):
    if request.method != 'POST':
        return redirect('orders:order-list')
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

def register_user(request):
    """
    Handle user signup using email as both username and email.
    Show a clear message if the email already exists.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, "✅ Account created successfully! Welcome aboard.")
                return redirect('orders:menu')
            except Exception as e:
                messages.error(request, str(e))
        else:
            # Show form validation errors (e.g., password mismatch)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})



def login_user(request):
    """
    Handle login using email and password.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('orders:menu')
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    """
    Log the user out and redirect to login page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('orders:login')


# ============================
# CHECKOUT PAGE
# ============================

@login_required
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('orders:menu')

    cart_items = []
    total_price = 0
    for item_id_str, qty in cart.items():
        product = get_object_or_404(Item, pk=int(item_id_str))
        subtotal = product.price * qty
        total_price += subtotal
        cart_items.append({'item': product, 'quantity': qty, 'subtotal': subtotal})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()

            from .models import OrderItem
            for row in cart_items:
                OrderItem.objects.create(
                    order=order,
                    item=row['item'],
                    quantity=row['quantity'],
                    price=row['item'].price,
                )

            request.session['cart'] = {}
            request.session.modified = True
            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect('orders:order-success', order_id=order.id)
    else:
        form = OrderForm(initial={'full_name': request.user.username})

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.user.is_authenticated and order.user and order.user != request.user:
        return redirect('orders:order-list')
    order_items = order.items.select_related('item').all()
    payment = order.payments.order_by('-created_at').first() if hasattr(order, 'payments') else None
    return render(request, 'orders/order_success.html', {
        'order': order,
        'order_items': order_items,
        'payment': payment,
    })


# ============================
# ADMIN DASHBOARD (CUSTOM)
# ============================

@staff_member_required
def dashboard_home(request):
    items = Item.objects.all().order_by('-created_at')
    orders = Order.objects.prefetch_related('items__item').order_by('-created_at')
    return render(request, 'dashboard/dashboard.html', {'items': items, 'orders': orders})

    
    


@staff_member_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfully!')
            return redirect('dashboard-home')
    else:
        form = ItemForm()
    return render(request, 'dashboard/add_item.html', {'form': form})


@staff_member_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('dashboard-home')
    else:
        form = ItemForm(instance=item)
    return render(request, 'dashboard/edit_item.html', {'form': form, 'item': item})


@staff_member_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    messages.success(request, 'Item deleted successfully!')
    return redirect('dashboard-home')

@staff_member_required
def order_dashboard(request):
    orders = Order.objects.prefetch_related('items__item').order_by('-created_at')
    return render(request, 'dashboard/order_dashboard.html', {'orders': orders})