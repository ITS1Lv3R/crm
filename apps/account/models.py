from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """ Создает и сохраняет пользователя с введенным им email и паролем """
        if not email:
            raise ValueError('email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', unique=True)
    first_name = models.CharField(verbose_name='name', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='surname', max_length=30, blank=True)
    user_phone = models.BigIntegerField(verbose_name='Номер телефона', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(verbose_name='registered', auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """ Возвращает first_name и last_name с пробелом между ними """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Возвращает сокращенное имя пользователя"""
        return self.first_name


class Manager(models.Model):
    POST_CHOISES = (
        ('Менеджер', 'Менеджер'),
        ('Старший менеджер', 'Старший менеджер'),
        ('Администратор', 'Администратор'),
    )
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    post = models.CharField(choices=POST_CHOISES, verbose_name="Должность", max_length=60)
    objects = UserManager()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

