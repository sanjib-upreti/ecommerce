from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import LoginForm, GuestForm
from address.models import Address
from orders.models import Order
from products.models import TestProduct
from address.forms import AddressForm

from accounts.models import UserProfile, GuestEmail
from cart.models import Cart
from billing.models import BillingProfile

# Create your views here.
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    #print(request.session.get('cart_id'))
    return render(request, "cart/cart.html", {"cart": cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = TestProduct.objects.get(id=product_id)
        except TestProduct.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            #added = False
        else:
            cart_obj.products.add(product_obj)  # cart_obj.products.add(product_id)
            #added = True
        request.session['cart_items'] = cart_obj.products.count()

    return redirect(reverse("cart:home"))

def cart_checkout(request):

    cart_obj, cart_created = Cart.objects.new_or_get(request)

    next_url = request.build_absolute_uri
    order_obj = None
    if cart_created or cart_obj.products.count()==0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    billing_address_form = AddressForm()
    shipping_address_id = request.session.get('shipping_address_id',None)

    billing_address_id = request.session.get('billing_address_id',None)

    # billing profile is creates or not is checked  up in billing profile model manager
    billing_profile,billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    # for card payemnt
    has_card = False

    if billing_profile is not None:
        if 'username' in request.session or 'guest_email_id' in request.session:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj,order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)

        if shipping_address_id :
            print("you are here shippping address")
            order_obj.shipping_address = Address.objects.get(id = shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id :
            print("you are here billing address")
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
            #print((order_obj))
        has_card = billing_profile.has_card()

    """if request.method =="POST":
        is_done = order_obj.check_done()  # calling manager method
        if is_done:
            order_obj.mark_paid() # calling manager methods
            request.session['cart_items']=0
            del request.session['cart_id']
            return redirect("cart:success")"""
    if request.method=="POST":
        is_ready = order_obj.check_done()
        if is_ready:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()  # sort a signal for us
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    '''
                    is this the best spot?
                    '''
                    billing_profile.set_cards_inactive()
                return redirect("cart:success")
            else:
                print(crg_msg)
                return redirect("cart:checkout")





    context = {"title": 'checkout',
               "object": order_obj,
               "form":login_form,
               "guest_form":guest_form,
               'billing_profile':billing_profile,
               "next_url":next_url,
               'billing_address_form':billing_address_form,
               'address_type':'shipping',
               'address_qs':address_qs,
               'has_card':has_card,
               'cart':cart_obj,
               }
    return render(request,'cart/checkout.html',context)


def cart_success(request):
    context={"title":"success"}
    return render(request,'cart/success.html',context)
