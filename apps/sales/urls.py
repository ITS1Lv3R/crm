from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('quests/<slug:slug>', views.QuestDetailView.as_view(), name='quest_detail'),
    path('search/', views.search, name='search'),
    path('orders_report/', views.orders_report, name='orders_report')

]
