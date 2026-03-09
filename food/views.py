from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Category, Food, Cart, Order, OrderItem


# ================= HOME & CATEGORY =================

def home(request):
    categories = Category.objects.all()
    return render(request, 'food/home.html', {'categories': categories})


def category(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    foods = Food.objects.filter(category=category, available=True)
    return render(request, 'food/category.html', {
        'category': category,
        'foods': foods
    })


# ================= AUTH =================

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'food/signup.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        return redirect('home')

    return render(request, 'food/signup.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'food/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'food/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ================= PROFILE =================

@login_required(login_url='/login/')
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'food/profile.html', {
        'orders': orders
    })


# ================= CART =================

@login_required(login_url='/login/')
def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        food=food
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required(login_url='/login/')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.food.price * item.quantity for item in cart_items)
    return render(request, 'food/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required(login_url='/login/')
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required(login_url='/login/')
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


# ================= PAYMENT PAGE =================

@login_required(login_url='/login/')
def payment_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart')

    total = sum(item.food.price * item.quantity for item in cart_items)
    return render(request, 'food/payment.html', {'total': total})


# ================= STEP 3: PLACE ORDER (COD)

@login_required(login_url='/login/')
def place_order(request):
    if request.method != "POST":
        return redirect('payment')

    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart')

    total = sum(item.food.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_price=total,
        status='pending',
        payment_method='cod'
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            food=item.food,
            quantity=item.quantity
        )

    cart_items.delete()

    return redirect('profile')


@login_required(login_url='/login/')
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

    
