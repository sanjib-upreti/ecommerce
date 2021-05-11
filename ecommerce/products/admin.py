from django.contrib import admin

from .models import TestProduct,Category,SubCategory,Review,Brand

# Register your models here.

class TestProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TestProduct._meta.fields if field.name != "id"]
    search_fields = [field.name for field in TestProduct._meta.fields if field.name != "id"]


admin.site.register(TestProduct,TestProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields if field.name != "id"]
    search_fields = [field.name for field in Category._meta.fields if field.name != "id"]
admin.site.register(Category,CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SubCategory._meta.fields if field.name != "id"]
    search_fields = [field.name for field in SubCategory._meta.fields if field.name != "id"]
admin.site.register(SubCategory,SubCategoryAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Brand._meta.fields if field.name != "id"]
    search_fields = [field.name for field in Brand._meta.fields if field.name != "id"]
admin.site.register(Brand,BrandAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Review._meta.fields if field.name != "id"]
    search_fields = [field.name for field in Review._meta.fields if field.name != "id"]

admin.site.register(Review,ReviewAdmin)
