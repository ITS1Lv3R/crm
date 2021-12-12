from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'user_phone', 'is_active', 'date_joined']
    list_filter = ['email', 'first_name', 'user_phone', 'is_active', 'date_joined']


admin.site.register(User, UserAdmin)

