from django.views.generic.detail import DetailView
from .models import Quest


class QuestDetailView(DetailView):
    """ Детальная вью для изображений"""
    model = Quest
    template_name = 'content/quest/quest_view.html'
    context_object_name = 'quest'
