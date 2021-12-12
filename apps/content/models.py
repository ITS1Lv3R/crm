from django.urls import reverse
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


def upload_path_quest_photo(instance, filename):
    return 'images/{0}/{1}'.format(instance, filename)


class Quest(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование квеста')
    slug = models.SlugField(max_length=200, blank=True)
    description = models.CharField(max_length=150, verbose_name='Описание квеста')
    image = ThumbnailerImageField('Фото', upload_to=upload_path_quest_photo, blank=True)
    duration = models.DurationField(verbose_name='Длительность квеста')
    difficulty = models.PositiveIntegerField(default=5,
                                             validators=[MinValueValidator(1), MaxValueValidator(5)],
                                             verbose_name='Сложность квеста')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена квеста')
    type = models.ForeignKey("TypeQuest",
                             related_name='quests',
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL, verbose_name='Тип')
    objects = BaseUserManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Квест'
        verbose_name_plural = 'Квесты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('content:quest_detail', args=[self.slug])

    def get_quest_value(self):
        """ Итоговая оценка квеста"""
        quest_feedbacks = QuestFeedBack.objects.filter(quest=self)
        count = QuestFeedBack.objects.filter(quest=self).count()
        total_value = sum(feedback.feedback_value.value for feedback in quest_feedbacks)
        if count > 0:
            quest_value = total_value / count
            return quest_value
        else:
            return 0

    get_quest_value.short_description = 'Оценка квеста'

    def get_all_feedback(self):
        """Все отзывы квеста"""
        return QuestFeedBack.objects.filter(quest=self)


class TypeQuest(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование типа')
    description = models.CharField(max_length=150, verbose_name='Описание типа', blank=True)
    objects = BaseUserManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип квеста'
        verbose_name_plural = 'Типы квеста'

    def __str__(self):
        return self.name


class QuestFeedBack(models.Model):
    description = models.CharField(max_length=500, verbose_name='Описание типа', blank=True)
    quest = models.ForeignKey("Quest",
                              related_name='feedbacks',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL, verbose_name='Отзыв о квесте')
    feedback_value = models.ForeignKey("FeedBackValue",
                                       related_name='feedback_value',
                                       null=True,
                                       blank=True,
                                       on_delete=models.SET_NULL, verbose_name='Оценка отзыва')
    objects = BaseUserManager()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Отзыв квеста'
        verbose_name_plural = 'Отзывы квеста'

    def __str__(self):
        return str(self.id)


class FeedBackValue(models.Model):
    value = models.IntegerField(verbose_name='Оценка в отзыве')
    objects = BaseUserManager()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Оценка отзыва'
        verbose_name_plural = 'Оценки для отзывов'

    def __str__(self):
        return str(self.id)
