from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'manager', 'comment', 'is_confirmed', 'time_start',
                    'time_finish', 'status', 'coupon',
                    Order.get_total_cost, Order.get_total_cost_discount, Order.get_discount_percent]
    list_filter = ['manager', 'is_confirmed', 'date_creation', 'time_start',
                   'time_finish', 'status', 'coupon']
    list_editable = ['status']


class CouponAdmin(admin.ModelAdmin):
    list_display = ['name', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['name', 'valid_from', 'valid_to', 'discount', 'active']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name', ]


class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']


admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Manager, ManagerAdmin)