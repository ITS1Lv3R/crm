from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class QuestAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'duration', 'price', 'type']
    list_filter = ['name', 'duration', 'price', 'type']
    prepopulated_fields = {'slug': ('name',)}
    exclude = ['order']


class TypeQuestAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name', ]


class QuestFeedBackAdmin(admin.ModelAdmin):
    list_display = ['quest', 'feedback_value']
    list_filter = ['quest', ]


class FeedBackValueAdmin(admin.ModelAdmin):
    list_display = ['value', ]


admin.site.register(Quest, QuestAdmin)
admin.site.register(TypeQuest, TypeQuestAdmin)
admin.site.register(QuestFeedBack, QuestFeedBackAdmin)
admin.site.register(FeedBackValue, FeedBackValueAdmin)