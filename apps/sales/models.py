from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

from ..account.models import User


class Order(models.Model):
    """ Модель для заказов пользователя"""
    client = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE,
                               verbose_name='Заказ Пользователя')
    comment = models.CharField('Комментарий к заказу', max_length=100)
    is_confirmed = models.BooleanField('Подвержден?', default=False)
    date_creation = models.DateTimeField(verbose_name='Дата создания заказа', auto_now_add=True)
    time_start = models.DateTimeField(verbose_name='Дата\Время старта')
    time_finish = models.DateTimeField(verbose_name='Дата\Время окончания')
    status = models.ForeignKey("Status",
                               related_name='status',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL, verbose_name='Статус')
    coupon = models.ForeignKey("Coupon",
                               related_name='coupons',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL, verbose_name='Купон')
    quests = models.ManyToManyField("Quest")
    objects = BaseUserManager()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return "Заказ № {}".format(self.id)

    def get_order_quests(self):
        quests = Quest.objects.filter(order=self)
        return quests

    def get_discount(self) -> int:
        if self.coupon:
            discount = self.coupon.discount
        else:
            discount = 0
        return discount

    def get_discount_percent(self):
        return "{} %".format(self.get_discount())

    get_discount_percent.short_description = 'Скидка'

    def get_total_cost(self):
        total_cost = sum(item.price for item in self.quests.all())
        return total_cost

    get_total_cost.short_description = 'Стоимость заказа'

    def get_total_cost_discount(self):
        total_cost = sum(item.price for item in self.quests.all())
        if self.get_discount() == 0:
            return total_cost
        else:
            return total_cost - total_cost * (self.get_discount() / Decimal('100'))

    get_total_cost_discount.short_description = 'Стоимость заказа со скидкой'


class Coupon(models.Model):
    name = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()
    objects = BaseUserManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование статуса')
    description = models.CharField(max_length=150, verbose_name='Описание статуса', blank=True)
    objects = BaseUserManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


def upload_path_quest_photo(instance, filename):
    return 'images/{0}/{1}'.format(instance, filename)


class Quest(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование квеста')
    slug = models.SlugField(max_length=200, blank=True)
    description = models.CharField(max_length=150, verbose_name='Описание квеста')
    image = ThumbnailerImageField('Фото', upload_to=upload_path_quest_photo, blank=True)
    duration = models.DurationField(verbose_name='Длительность квеста')
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
        return reverse('sales:quest_detail', args=[self.slug])


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
