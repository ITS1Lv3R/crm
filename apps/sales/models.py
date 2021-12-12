from decimal import Decimal
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from ..account.models import User
from ..content.models import Quest


class Order(models.Model):
    """ Модель для заказов пользователя"""
    client = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE,
                               verbose_name='Заказ Пользователя')
    manager = models.ForeignKey("Manager", related_name='orders_manager', on_delete=models.CASCADE,
                                verbose_name='Менеджер')
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
    quest = models.ForeignKey(Quest,
                              related_name='quest',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL, verbose_name='Квест')
    count_players = models.PositiveIntegerField(default=2,
                                                validators=[MinValueValidator(1), MaxValueValidator(5)],
                                                verbose_name='Количество игроков')
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
        return self.quest.price

    get_total_cost.short_description = 'Стоимость заказа'

    def get_total_cost_discount(self):
        total_cost = self.quest.price
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


class Manager(models.Model):
    POST_CHOISES = (
        ('Менеджер', 'Менеджер'),
        ('Старший менеджер', 'Старший менеджер'),
        ('Администратор', 'Администратор'),
    )
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    post = models.CharField(choices=POST_CHOISES, verbose_name="Должность", max_length=60)
    objects = BaseUserManager()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        ordering = ('post',)
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

    def get_all_sales(self):
        """ все продажи менеджера за всё время"""
        return Order.objects.filter(manager=self)
