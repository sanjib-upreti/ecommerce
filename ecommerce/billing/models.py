from django.db import models


# Create your models here.
from django.db.models.signals import post_save, pre_save

from accounts.models import UserProfile, GuestEmail
# for payement gateway
" import stripe and add your secret test key here"
import stripe
stripe.api_key="sk_test_OvjR2MfvkfBoOelUDfVYfjDr00XOFHZ4hX"
# for payment gateway


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = None
        if 'username' in request.session:
            user = UserProfile.objects.get(email=request.session['username'])
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user is not None:
            'logged in user checkout; remember payment details'
            obj, created = self.model.objects.get_or_create(
                            user=user, email=user.email)
        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment details'
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                                            email=guest_email_obj.email)
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user           = models.OneToOneField(UserProfile,null=True,blank=True,on_delete=models.CASCADE)
    email          = models.EmailField()
    active         = models.BooleanField(default=True)
    timestamp      = models.DateTimeField(auto_now_add=True)
    update         = models.DateTimeField(auto_now=True)

    """ for payment gateway create later"""
    customer_id = models.CharField(max_length=120, null=True, blank=True)
    # customer_id for creating a customer for stripe

    objects = BillingProfileManager()



    def __str__(self):
        return self.email

    """ for payment gateway and payment """

    def get_cards(self):
        cards = Card.objects.filter(billing_profile=self)
        return cards



    def has_card(self):  # instance.has_card
        card_qs = self.get_cards()
        #print("you are here")
        #print(card_qs.exists())
        return card_qs.exists()  # True or False


    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()

    """ for charging with card """

    def charge(self, order_obj, card=None):
        return Charge.objects.pay(self, order_obj, card)

""" creating a customer unique customer id for stripe payment """

def billing_profile_created_receiver(sender,instance,*args,**kwargs):
    if not instance.customer_id and instance.email:
        print("ACTUAL API REQUEST Send to stripe/braintree")
        customer = stripe.Customer.create(
            email=instance.email
        )
        """ creates a customer on stripe with your secret api key"""
        print(customer)
        instance.customer_id = customer.id
""" pre save signal to Billing Profile"""
pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)

def user_created_reciever(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)
post_save.connect(user_created_reciever,sender=UserProfile)


class CardManager(models.Manager):
    def all(self, *args, **kwargs): # ModelKlass.objects.all() --> ModelKlass.objects.filter(active=True)
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, token):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            stripe_card_response = customer.sources.create(source=token)
            new_card = self.model(
                    billing_profile=billing_profile,
                    stripe_id = stripe_card_response.id,
                    brand = stripe_card_response.brand,
                    country = stripe_card_response.country,
                    exp_month = stripe_card_response.exp_month,
                    exp_year = stripe_card_response.exp_year,
                    last4 = stripe_card_response.last4
                )
            new_card.save()
            return new_card
        return None



class Card(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    stripe_id               = models.CharField(max_length=120)
    brand                   = models.CharField(max_length=120, null=True, blank=True)
    country                 = models.CharField(max_length=20, null=True, blank=True)
    exp_month               = models.IntegerField(null=True, blank=True)
    exp_year                = models.IntegerField(null=True, blank=True)
    last4                   = models.CharField(max_length=4, null=True, blank=True)
    default                 = models.BooleanField(default=True)
    active                  = models.BooleanField(default=True)
    timestamp               = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)




def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)


post_save.connect(new_card_post_save_receiver, sender=Card)





class ChargeManager(models.Manager):
    def pay(self, billing_profile, order_obj, card=None): # Charge.objects.pay()
        card_obj = card
        if card_obj is None:
            card_obj = billing_profile.default_card();
        if card_obj is None:
            return False, "No cards available"
        c = stripe.Charge.create(
              amount = int(order_obj.total * 100), # 39.19 --> 3919
              currency = "inr",
              customer =  billing_profile.customer_id,
              source = card_obj.stripe_id,
              metadata={"order_id":order_obj.order_id},
            )
        new_charge_obj = self.model(
                billing_profile = billing_profile,
                stripe_id = c.id,
                paid = c.paid,
                refunded = c.refunded,
                outcome = c.outcome,
                outcome_type = c.outcome['type'],
                seller_message = c.outcome.get('seller_message'),
                risk_level = c.outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message


class Charge(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id               = models.CharField(max_length=120)
    paid                    = models.BooleanField(default=False)
    refunded                = models.BooleanField(default=False)
    outcome                 = models.TextField(null=True, blank=True)
    outcome_type            = models.CharField(max_length=120, null=True, blank=True)
    seller_message          = models.CharField(max_length=120, null=True, blank=True)
    risk_level              = models.CharField(max_length=120, null=True, blank=True)
    objects = ChargeManager()