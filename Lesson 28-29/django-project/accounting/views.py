from django.contrib.auth.decorators import login_not_required
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.views import LoginView
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .forms import RegisterForm
from .models import User
from .api.serializers import UserSerializer

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

class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Пользователь успешно создан",
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
