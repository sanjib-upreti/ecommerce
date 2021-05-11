from django.contrib import admin

# Register your models here.
from address.models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Address._meta.fields if field.name != "id"]
    search_fields = ['address_line_1','city','state','address_line_2','address_type']


admin.site.register(Address,AddressAdmin)
