from django.urls import path
from . import views

urlpatterns = [
    path('productpage/', views.product_page),
    path('productcategory/<id>', views.productcategory_page),
    path('productdetails/<id>', views.product_details),

]