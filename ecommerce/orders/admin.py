from django.contrib import admin
from .models import Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields if field.name != "id"]
    list_display_links = ['order_id']
admin.site.register(Order, OrderAdmin)

