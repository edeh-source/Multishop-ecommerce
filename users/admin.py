from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone_number', 'first_name', 'last_name']
    list_filter = ['email', 'phone_number']
    