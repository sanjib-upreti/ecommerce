from django.db import models
from decimal import Decimal
from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver

from accounts.models import UserProfile
from products.models import  TestProduct

# Create your models here.

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            cart_created = False
            cart_obj = qs.first()
            if request.session.get('username') is not None and cart_obj.user is None:
                try:
                    cart_obj.user = UserProfile.objects.get(email=request.session.get("username")).id
                except:
                    cart_obj.user=None

                cart_obj.save()
        else:
            try:
                user =UserProfile.objects.get(email=request.session.get("username"))
                # changes by me
            except:
                user = None
            cart_obj = Cart.objects.new(request,user=user)
            cart_created = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, cart_created

    def new(self, request,user=None):
        user_obj = None
        if user is not None:
            if request.session.get('username'):
                user_obj = user
        return self.model.objects.create(user=user_obj)




class Cart(models.Model):
    user        = models.ForeignKey(UserProfile, null=True, blank=True,on_delete=models.CASCADE)
    products    = models.ManyToManyField(TestProduct, blank=True)
    subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    objects = CartManager()

    def __str__(self):
        return str(self.id)+str(self.products)

def m2m_updated_cart(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for product in products:
            total += product.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_updated_cart, sender=Cart.products.through)




def pre_save_cart_total_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) * Decimal(1.10) # 8% tax
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_total_receiver, sender=Cart)




