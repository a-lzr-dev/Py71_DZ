from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegisterForm, PasswordResetRequestForm
from .models import User


class CustomLoginView(LoginView):
    template_name = "accounting/login.html"

@login_not_required
def register_user_view(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password1'],
            )
            return redirect(resolve_url("account-login"))

    return render(request, "accounting/register.html", {"form": form})

def password_reset_request(request):
    # Сброс пароля по email
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # вместо отправки письма переход на страницу сброса
                return redirect(reverse('accounting:password-reset-confirm', kwargs={'uidb64': uid, 'token': token}))
            return render(request, 'accounting/password_reset_done.html')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounting/password_reset_form.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    # Ввод и подтверждение нового пароля
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect(resolve_url('accounting:login'))
        else:
            form = SetPasswordForm(user)
        return render(request, 'accounting/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'accounting/password_reset_invalid.html')
