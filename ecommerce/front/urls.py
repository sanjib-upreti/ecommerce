
from django.urls import path
from . import views

app_name='front'
urlpatterns = [
    path('', views.index,name='home'),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path('login/', views.login_page,name='login'),
    path('register/', views.register_page,name='register'),

]