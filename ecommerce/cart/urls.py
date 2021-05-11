from django.urls import path
from . import views

app_name = 'cart'


urlpatterns = [

    path('cart/', views.cart_home,name='home'),
    path('cart/update/', views.cart_update,name='update'),
    path('cart/checkout/', views.cart_checkout,name='checkout'),
    path('cart/success/', views.cart_success,name='success'),
]