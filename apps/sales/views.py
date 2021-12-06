from django.contrib import messages
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import *
from django.db.models import Q


class IndexView(ListView):
    """ Вью для главной страницы, все квесты"""
    queryset = Quest.objects.all()
    template_name = 'sales/index.html'
    context_object_name = 'quests'
    paginate_by = 6


class QuestDetailView(DetailView):
    """ Детальная вью для изображений"""
    model = Quest
    template_name = 'sales/quest/quest_view.html'
    context_object_name = 'quest'


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
