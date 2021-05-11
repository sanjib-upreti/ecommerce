from django.contrib import admin

# Register your models here.
from billing.models import BillingProfile,Card



class BillingProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BillingProfile._meta.fields if field.name != "id"]
    search_fields = [field.name for field in Card._meta.fields if field.name != "id"]

admin.site.register(BillingProfile,BillingProfileAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Card._meta.fields if field.name != "id"]
    search_fields = [field.name for field in Card._meta.fields if field.name != "id"]

admin.site.register(Card,CartAdmin)
