from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
from django.utils.http import is_safe_url

from accounts.models import UserProfile, GuestEmail
from cart.models import Cart
from orders.models import Order
from .forms import LoginForm, GuestForm
from .forms import UserProfileForm


def register_user(request):
    userprofileform = UserProfileForm(request.POST or None)

    if request.method == "POST":

        if userprofileform.is_valid():
            try:
                userprofileform.save()
                return redirect('/loginuser')
            except:
                return redirect('/unsuccessful')


    context = {"title": "User Registration",
               "form": userprofileform}
    return render (request,'front/userprofile.html',context)




def login_user(request):
    login_form = LoginForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        try:
            user = UserProfile.objects.get(email = username, password=password)
            request.session['username'] = username

        except:
            return redirect('/loginuser')


        if user is not None:
            try:
                del request.session['guest_email_id']
                del request.session['guest_email']
            except:
                pass
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/productpage')
        else:
            return redirect('/loginuser')
    context = {"title": "Login || ecommerce",
               "form": login_form,
               }


    return render(request, 'front/login.html', context)


def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect('/loginuser')


def guest_register_user(request):
    guest_form = GuestForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if request.method =='POST':
        if guest_form.is_valid():
            email = guest_form.cleaned_data.get("username")
            new_guest_email = GuestEmail.objects.create(email=email)
            request.session['guest_email_id'] = new_guest_email.id
            request.session['guest_email']= email
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect(reverse('accounts:registeruser'))



    return redirect(reverse('accounts:registeruser'))


def orderhistory(request):
    orderhistory = Order.objects.filter(billing_profile__email=request.session.get('username'))


    context={
        'titile':"Order History",
        'orderhistory':orderhistory
    }
    return render(request,'accounts/orderhistory.html',context)



def orderdetails(request,order_id):
    orderhistory = Order.objects.get(order_id=order_id)
    cartid = orderhistory.cart.id
    cartproducts = Cart.objects.get(id=cartid)

    context={
        'titile':"Order History",
        'cartproducts':cartproducts,

    }
    return render(request,'accounts/orderdetails.html',context)


