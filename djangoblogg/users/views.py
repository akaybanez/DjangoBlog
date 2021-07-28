from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.views.generic.base import TemplateView
from .forms import LoginForm, SignupForm


class SignupView(TemplateView):
    def get(self, request):
        form = SignupForm()

        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get(
                'email')  # validate form input fields
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)

            form.save()
            login(request, user)

            return redirect('blog:dashboard')
        else:
            return render(request, 'users/signup.html', {'form': form})


class LoginView(TemplateView):

    def get(self, request):
        loginform = LoginForm()

        return render(request, 'users/login.html', {'form': loginform})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            # check if user is valid
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('blog:dashboard')
            else:
                return render(request, 'users/login.html', {'form': form})
        else:
            return render(request, 'users/login.html', {'form': form})


def LogoutView(request):
    logout(request)

    return redirect('users:login')
