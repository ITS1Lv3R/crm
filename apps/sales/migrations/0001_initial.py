# Generated by Django 3.1.6 on 2021-12-05 14:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('active', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Купон',
                'verbose_name_plural': 'Купоны',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование статуса')),
                ('description', models.CharField(blank=True, max_length=150, verbose_name='Описание статуса')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TypeQuest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование типа')),
                ('description', models.CharField(blank=True, max_length=150, verbose_name='Описание типа')),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование квеста')),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('description', models.CharField(max_length=150, verbose_name='Описание квеста')),
                ('duration', models.DurationField(verbose_name='Длительность квеста')),
                ('price', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Цена квеста')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quests', to='sales.typequest', verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Квест',
                'verbose_name_plural': 'Квесты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=100, verbose_name='Комментарий к заказу')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='Подвержден?')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('time_start', models.DateTimeField(verbose_name='Дата\\Время старта заказа')),
                ('time_finish', models.DateTimeField(verbose_name='Дата\\Время окончания заказа')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Заказ Пользователя')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coupons', to='sales.coupon', verbose_name='Купон')),
                ('quests', models.ManyToManyField(to='sales.Quest')),
                ('status', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='status', to='sales.status', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('id',),
            },
        ),
    ]