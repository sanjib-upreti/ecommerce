from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from accounts.forms import LoginForm
from .forms import ContactForm,  RegisterForm
# using django authentication and login
from django.contrib.auth import authenticate, login
# importing User model from django.contrib.auth.models
from django.contrib.auth.models import User







# Create your views here.

def index(request):
    context = {"title": "Home || ecommerce"}
    return render(request, 'front/index.html', context)


def about(request):
    context = {"title": "About || ecommerce"}

    return render(request, 'front/about.html', context)


def contact(request):
    # to pass the data through form by classes in form
    contact_form = ContactForm(request.POST or None)
    context = {"title": "Contact || ecommerce",
               "form": contact_form

               }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    # handling form data here
    # if(request.method=="POST"):
    # 	name = request.POST.get("name")
    # 	name = request.POST.get("email")
    # 	name = request.POST.get("message")
    return render(request, 'front/contact.html', context)


def login_page(request):
    login_form = LoginForm(request.POST or None)



    if login_form.is_valid():
        print(login_form.cleaned_data)

        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # redirect to success page
            # context['form']=LoginForm()
            return redirect('/productpage')
        else:

            return redirect('/login')
    context = {"title": "Login || ecommerce",
               "form": login_form,
               }


    return render(request, 'front/login.html', context)


def register_page(request):
    register_form = RegisterForm(request.POST or None)

    context = {"title": "Register || ecommerce",
               "form": register_form,
               }

    if register_form.is_valid():
        print(register_form.cleaned_data)

        username = register_form.cleaned_data.get("username")
        password = register_form.cleaned_data.get("password")
        email = register_form.cleaned_data.get("email")
        first_name = register_form.cleaned_data.get("name")

        created =User.objects.create_user(username=username, password=password, email=email,first_name=first_name)

        if created:

            return redirect('/login')
        else:

            return redirect('/register')

    return render(request, 'front/register.html', context)












