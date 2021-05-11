from django.urls import path
from . import views

app_name = 'address'


urlpatterns = [
    path('checkout_address/', views.checkout_address,name='checkout_address'),
    path('checkout_address_reuse/', views.checkout_address_reuse,name='checkout_address_reuse'),
]