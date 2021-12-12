from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.contrib.auth import logout


def user_login(request):
    """Функция для авторизации юзера"""
    if request.method == 'POST':
        user = authenticate(request,
                            email=request.POST.get('email'),
                            password=request.POST.get('password'))
        if user:  # Проверяем есть ли юзер в бд
            if user.is_active:  # Проверяем активен ли юзер
                login(request, user)
                messages.success(request, 'Вы успешно авторизовались на сайте!')
                return redirect('sales:index')  # Если всё ок, отправляем юзера на главную страницу
            else:
                messages.error(request, 'Аккаунт неактивен!')
                return redirect('login')
        else:
            messages.error(request, 'Неверные логин или пароль')
            redirect('login')

    context = locals()
    template = 'account/login.html'
    return render(request, template, context)


def user_logout(request):
    """Функция для логаута"""
    logout(request)
    template = 'account/logged_out.html'
    return render(request, template)


def register(request):
    """Функция для регистрации юзера"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        # проверяем на валидность форму юзера
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user_email = user_form.cleaned_data["email"]

            # Получаем имя пользователя из его email
            new_user.first_name = new_user_email.split('@')
            new_user.first_name = new_user.first_name[0]

            # если валидна, то создаём юзера
            new_user.save()
            # После создания юзера и профиля отправляем пользователя в личный кабинет
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Вы успешно зарегистрировались на сайте!')
            return redirect('sales:index')
        else:
            messages.error(request, 'Пользователь с таким email уже существует')
            return redirect('register')

    else:
        user_form = UserRegistrationForm()
    context = locals()
    template = 'account/register.html'
    return render(request, template, context)


@login_required
def profile(request):
    """Функция личного кабинета"""
    # блок для редактирования профиля
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Ваш Профиль успешно изменён')
    else:
        user_form = UserProfileForm(instance=request.user)

    user = request.user

    context = locals()
    template = 'account/profile.html'
    return render(request, template, context)
