from django.contrib import admin
from .models import Company, CompanyAddress

# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'slug', 'inn', 'created', 'updated')
    list_filter = ('user', 'title', 'created')
    ordering = ('user', 'created', 'updated')



@admin.register(CompanyAddress)
class CompanyAddressAdmin(admin.ModelAdmin):
    list_display = ('company', 'city', 'district', 'address', 'email', 'tel1', 'main_add')
    list_filter = ('company', 'district', 'city')
    ordering = ('id', 'company', 'city')