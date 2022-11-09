from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets+ (
        (      
            'Custom fields', # you can also use None                 
            {
                'fields': (
                    'status',
                    'is_deleted',
                ),
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'image', 'date_of_birth', 'tel', 'city', 'company')
    list_filter = ('user', 'created', 'city')
    ordering = ('user', 'created', 'city')

