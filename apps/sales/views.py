from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from .models import *
from django.db.models import Q
from ..content.models import Quest


class IndexView(ListView):
    """ Вью для главной страницы, все квесты"""
    queryset = Quest.objects.all()
    template_name = 'sales/index.html'
    context_object_name = 'quests'
    paginate_by = 6


def page_not_found(request, exception):
    template = 'core/404.html'
    status = 404
    context = locals()
    return render(request, template, context)


def page_not_found_500(request):
    template = 'core/500.html'
    status = 500
    context = locals()
    return render(request, template, context)


def search(request):
    """ функция поиска """
    query = request.GET.get('q')
    # изменяем регистр первого символа запроса. проанализировать надо будет
    query = query.title()
    quests = Quest.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'sales/search.html', {'quests': quests,
                                                 'query': query})


def get_orders_total_count():
    """ функция, рассчитывающая итоговое количество заказов за весь период"""
    return Order.objects.all().count()


def get_total_sum_all_orders():
    """ функция, рассчитывающая итоговую сумму по всем заказам со скидкой"""
    total_sum = sum(order.get_total_cost_discount() for order in Order.objects.all())
    return total_sum


def orders_report(request):
    """ Отчет по продажам"""
    orders = Order.objects.all()
    orders_total_count = get_orders_total_count()
    total_sum_all_orders = get_total_sum_all_orders()

    context = locals()
    return render(request, 'sales/orders_report.html', context)


def order_create(request, slug):
    """ Заглушка на форму заказа квеста"""
    quest = Quest.objects.get(slug=slug)
    if request.user.is_authenticated:
        Order.objects.create(quest=quest,
                             client=request.user,
                             time_start="2021-12-09 14:00:00",
                             time_finish="2021-12-09 15:00:00",
                             status=Status.objects.get(name='Новый'),
                             manager=Manager.objects.get(id=1)
                             )
        messages.success(request, "Вы успешно заказали квест!")
        return redirect('content:quest_detail', quest.slug)
    else:
        messages.error(request, "Для заказа квеста авторизуйтесь на сайте")
        return redirect('login')
