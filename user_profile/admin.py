# user_profile/admin.py
from django.contrib import admin
from . import models


@admin.register(models.User)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('email',  
                    'created_at', 
                    'id',  
                    'first_name',  
                    'phone_number',  
                    'is_email_verified',
                    'is_staff', 
                    'is_superuser', 
                    )
    