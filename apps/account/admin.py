from django.contrib import admin
from .models import User, Manager


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'user_phone', 'is_active', 'date_joined']
    list_filter = ['email', 'first_name', 'user_phone', 'is_active', 'date_joined']


class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']


admin.site.register(User, UserAdmin)
admin.site.register(Manager, ManagerAdmin)
