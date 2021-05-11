from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from django.urls import reverse

from billing.models import BillingProfile, Card

" import stripe and add your secret test key here"
import stripe
stripe.api_key="sk_test_OvjR2MfvkfBoOelUDfVYfjDr00XOFHZ4hX"
STRIPE_PUBLISH_KEY ="pk_test_babMK6n6rBv0q4M5h3wSgrep00CGBokpjM"

# Create your views here.
def payment_method(request):
    """ if 'username' in request.session or 'guest_email_id' in request.session:
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        my_customer_id = billing_profile.customer_id """
    billing_profile,billing_profile_created = BillingProfile.objects.new_or_get(request)
    has_card = None;
    if not billing_profile:
        return redirect("cart:home")
    else:
        try:
            cards = Card.objects.filter(billing_profile=billing_profile,active=True)
            has_card = True
        except:
            has_card= None;

    next_url = None
    next_ = request.GET.get('next')
    #print(next)
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    context={"publish_key":STRIPE_PUBLISH_KEY,
             "next_url": next_url,
             "has_card":has_card,
             "cards":cards,
             }
    return render(request,'billing/payment-method.html',context)

def payment_method_create(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status_code=401)
        token = request.POST.get("token")
        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)
        return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse("error", status_code=401)


def updatedefaultcard(request):
    if request.method=="POST":
        cardid = request.POST.get("cardid")
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return redirect("cart:home")
        else:
            qs = Card.objects.filter(billing_profile=billing_profile).exclude(id=cardid)
            qs.update(default=False)
            card = Card.objects.get(id = cardid)
            card.default= True
            card.save()
    return redirect(reverse("cart:checkout"))

