from django.shortcuts import render, redirect
from django.views import View 
from .models import User  
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout

class RegisterView(View):


    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'users/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'users/register.html', {'error': 'As senhas não coincidem'})

        if User.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {'error': 'Email já cadastrado'})

        user = User(email=email, password=make_password(password), username=username)
        user.save()

        return redirect('login')

class LoginView(View):


    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'users/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)  
            return redirect('dashboard')
        return render(request, 'users/login.html', {'error': 'Credenciais inválidas'})

class LogoutView(View):


    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')