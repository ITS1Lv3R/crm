from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'comment', 'is_confirmed', 'time_start',
                    'time_finish', 'status', 'coupon',
                    Order.get_total_cost, Order.get_total_cost_discount, Order.get_discount_percent]
    list_filter = ['id', 'client', 'comment', 'is_confirmed', 'date_creation', 'time_start',
                   'time_finish', 'status', 'coupon']
    list_editable = ['status']


class CouponAdmin(admin.ModelAdmin):
    list_display = ['name', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['name', 'valid_from', 'valid_to', 'discount', 'active']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name', ]


class QuestAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'duration', 'price', 'type']
    list_filter = ['name', 'duration', 'price', 'type']
    prepopulated_fields = {'slug': ('name',)}
    exclude = ['order']


class TypeQuestAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name', ]


admin.site.register(Quest, QuestAdmin)
admin.site.register(TypeQuest, TypeQuestAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Status, StatusAdmin)
