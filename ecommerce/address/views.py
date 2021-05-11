from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from address.models import Address
from billing.models import BillingProfile
from cart.models import Cart
from orders.models import Order
from .forms import AddressForm

# Create your views here.

def checkout_address(request):
    addressform = AddressForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if request.method == "POST":

        if addressform.is_valid():
            instance = addressform.save(commit=False)
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if billing_profile is not None:
                address_type=request.POST.get('address_type','shipping')
                instance.billing_profile = billing_profile
                instance.address_type = address_type
                instance.save()
                request.session[address_type+'_address_id']= instance.id
                #print(address_type)

            else:
                return redirect('cart:checkout')

            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('cart:checkout')
    return redirect('cart:checkout')



def checkout_address_reuse(request):
    if 'username' in request.session or 'guest_email_id' in request.session:

        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        if request.method == "POST":
            print(request.POST)
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping_address')
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + "_id"] = shipping_address
                    if address_type=="shipping_address":
                        order_obj.shipping_address = Address.objects.get(id = shipping_address)
                    elif address_type=="billing_address":
                        order_obj.billing_address = Address.objects.get(id=shipping_address)

                    order_obj.save()

                    del request.session[address_type + "_id"]

                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect("cart:checkout")





