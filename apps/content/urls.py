from django.urls import path
from . import views

app_name = 'content'


urlpatterns = [
    path('quests/<slug:slug>', views.QuestDetailView.as_view(), name='quest_detail')
]

