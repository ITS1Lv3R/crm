# Generated by Django 3.1.6 on 2021-12-05 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.CharField(max_length=100, verbose_name='Комментарий к заказу'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='status', to='sales.status', verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='time_finish',
            field=models.DateTimeField(verbose_name='Дата\\Время окончания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='time_start',
            field=models.DateTimeField(verbose_name='Дата\\Время старта'),
        ),
    ]
