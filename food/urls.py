from django.urls import path
from . import views

urlpatterns = [
    # Home & Category
    path('', views.home, name='home'),
    path('category/<str:category_name>/', views.category, name='category'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Cart
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),

    # Orders
    path('place-order/', views.place_order, name='place_order'),

    path('profile/', views.profile_view, name='profile'),

    

    #payment
    path('payment/', views.payment_page, name='payment'),

]
