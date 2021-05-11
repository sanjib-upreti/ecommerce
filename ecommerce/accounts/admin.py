from django.contrib import admin

# Register your models here.

from .models import UserProfile,GuestEmail

class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields if field.name != "id" and field.name !='password' and field.name!='confirm_password']

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(GuestEmail)