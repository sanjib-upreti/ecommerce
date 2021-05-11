from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('registeruser/', views.register_user, name='registeruser'),
    path('loginuser/', views.login_user, name='loginuser'),
    path('logout/', views.logout, name='logout'),
    path('guest_register/',views.guest_register_user,name='guest_register'),
    path('orderhistory/',views.orderhistory,name='orderhistory'),
    path('orderdetails/<order_id>',views.orderdetails,name='orderdetails')

]

