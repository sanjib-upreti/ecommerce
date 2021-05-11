from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import random
import os

# Create your models here.

# to change the name of file before uploading a file
from django.db.models.signals import pre_save

from ecommerce.utils import unique_slug_generator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name,ext = os.path.splitext(base_name)
    return name,ext



def upload_image_path(instance,filename):
    new_filename = random.randint(1,6763373383838)
    name,ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    #fortmat(new_filename=new_filename,ext=ext)
    return  'myproduct/'+f"{new_filename}/{final_filename}"

def upload_category_image_path(instance,filename):
    new_filename = random.randint(1,6763373383838)
    name,ext = get_filename_ext(filename)
    final_filename = f"cat{new_filename}{ext}"
    #fortmat(new_filename=new_filename,ext=ext)
    return  'categoryimage/'+f"{final_filename}"

def upload_subcategory_image_path(instance,filename):
    new_filename = random.randint(1,6763373383838)
    name,ext = get_filename_ext(filename)
    final_filename = f"sub{new_filename}{ext}"
    #fortmat(new_filename=new_filename,ext=ext)
    return  'subcategoryimage/'+f"{final_filename}"

def upload_brand_image_path(instance,filename):
    new_filename = random.randint(1,6763373383838)
    name,ext = get_filename_ext(filename)
    final_filename = f"cat{new_filename}{ext}"
    #fortmat(new_filename=new_filename,ext=ext)
    return  'brand/'+f"{final_filename}"


class Category(models.Model):
    categoryname = models.CharField(max_length=80,unique=True)
    categoryimage = models.ImageField(upload_to=upload_category_image_path,null=True,blank=True)

    def __str__(self):
        return self.categoryname

class SubCategory(models.Model):
    categoryname = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategoryname = models.CharField(max_length=30)
    subcategoryimage = models.ImageField(upload_to=upload_subcategory_image_path,null=True,blank=True)

    def __str__(self):
        return self.categoryname.categoryname + ' - ' +self.subcategoryname

class Brand(models.Model):
    brandname = models.CharField(max_length=80, unique=True)
    brandimage = models.ImageField(upload_to=upload_brand_image_path, null=True, blank=True)

    def __str__(self):
        return  self.brandname


class TestProduct(models.Model):

    title = models.CharField(max_length=80)
    brand = models.ForeignKey(Brand,on_delete=models.DO_NOTHING,default=1)

    description = models.TextField()
    qtysizeS=models.IntegerField(default=10)
    qtysizeM=models.IntegerField(default=10)
    qtysizeL=models.IntegerField(default=10)
    sizeXL=models.IntegerField(default=10)
    price = models.DecimalField(decimal_places=2,max_digits=15)
    image = models.ImageField(upload_to=upload_image_path,default='default.jpg')
    subcategory = models.ForeignKey(SubCategory,on_delete= models.CASCADE ,default=1)
    discount = models.IntegerField(default=0,validators=[
            MaxValueValidator(99),
            MinValueValidator(0)
        ])
    slug = models.SlugField(max_length=250, null=True, blank=True)
    active = models.BooleanField(default= True)


    def __str__(self):
        return self.title + self.description + str(self.price)


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=TestProduct)




class Review(models.Model):
    reviewby = models.CharField(max_length=80)
    description = models.TextField()
    productid = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['reviewby', 'productid'], name='uniquereviewconstraint')
        ]

    def __str__(self):
        return self.reviewby+" , "+str(self.productid)+" , "+self.description+" , "+str(self.created_at)+""







