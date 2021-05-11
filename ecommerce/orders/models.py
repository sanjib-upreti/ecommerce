from django.db import models
from django.db.models.signals import pre_save, post_save

from address.models import Address
from billing.models import BillingProfile
from cart.models import Cart
from ecommerce.utils import unique_order_id_generator

# Create your models here.

ORDER_STATUS_CHOICES =(('created','Created'),
                       ('paid','Paid'),
                       ('shipped','Shipped'),
                       ('refunded','Refunded'),)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True,
            status='created'
        )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile,
                cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model):
    billing_profile    = models.ForeignKey(BillingProfile,on_delete=models.CASCADE,null=True,blank=True)
    shipping_address   = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.CASCADE, null=True,
                                         blank=True)
    billing_address    = models.ForeignKey(Address, related_name='billing_address', on_delete=models.CASCADE, null=True,
                                        blank=True)

    # for time being we are setting it to null and blank = true
    order_id           = models.CharField(max_length=120)
    cart               = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status             = models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    shipping_total     = models.DecimalField(default=100,max_digits=100,decimal_places=2)
    total              = models.DecimalField(default=100,max_digits=100,decimal_places=2)
    active             = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id + "     "+ str(self.billing_profile.email)+"     "+ str(self.cart.id)

    def update_total(self):
        cart_total = self.cart.total

        if self.cart.subtotal >1000:
            self.shipping_total=0
        else:
            self.shipping_total=100


        new_total = cart_total + self.shipping_total
        print("new total ",new_total)
        self.total=new_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        shipping_address = self.shipping_address
        total = self.total
        if billing_profile and shipping_address and billing_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status ="paid"
            self.save()
        return self.status



def pre_save_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id,sender=Order)


def post_save_cart_total(sender,instance,*args,**kwargs):
    cart_obj= instance
    cart_total= cart_obj.total
    cart_id = cart_obj.id
    qs = Order.objects.filter(cart__id = cart_id)
    print("counting",qs.count())
    if qs.count()== 1:
        order_obj = qs.first()
        order_obj.update_total()

post_save.connect(post_save_cart_total,sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):

    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)


