from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.search, name='search'),
    path('orders_report/', views.orders_report, name='orders_report'),
    path('order_create/<slug:slug>', views.order_create, name='order_create')
]
