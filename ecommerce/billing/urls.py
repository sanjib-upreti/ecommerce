from django.urls import path
from . import views

app_name = 'billing'


urlpatterns = [

    path('payment_method/', views.payment_method,name='payment-method'),
    path('payment_method_create/', views.payment_method_create, name='payment-method-create'),
    path('updatedefaultcard/',views.updatedefaultcard,name='updatedefaultcard')

]