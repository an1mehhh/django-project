import random
import string

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, CustomPasswordResetForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        verification = gen_verification_code_or_password()
        new_user.email_verification = verification
        new_user.is_active = False
        if new_user.email_verification != verification or new_user.is_active != False:
            new_user.save(update_fields=['email_verification', 'is_active'])
        else:
            new_user.save()

        verification_url = f'http://127.0.0.1:8000/users/activate/{verification}'

        # Отправка письма
        send_mail(
            subject='Подтверждение почты',
            message=f'Подтвердите вашу почту. Перейдите по ссылке: {verification_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )

        return super().form_valid(form)


class ProfileView(DetailView):
    model = User
    template_name = 'users/profile_detail.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(View):
    model = User
    template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        form = CustomPasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                # Генерация нового пароля
                new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                user.password = make_password(new_password)
                user.save()

                # Отправка нового пароля по электронной почте
                send_mail(
                    subject='Ваш новый пароль',
                    message=f'Ваш новый пароль: {new_password}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                return redirect(self.success_url)
            else:
                return HttpResponse('Пользователь с таким адресом электронной почты не найден.', status=404)
        return render(request, self.template_name, {'form': form})


# генерирует случайный код подтверждения или пароль длиной 12 символов.
def gen_verification_code_or_password():
    return ''.join([str(random.randint(0, 9)) for i in range(12)])


# активация пользователя
def activate_user(request, verification_code):
    user = get_object_or_404(User, email_verification=verification_code)
    user.is_active = True
    user.email_verification = ''
    user.save()
    return render(request, 'users/activation_success.html')
