from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .models import User
from .forms import RegisterForm


class AppLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy("management_sys:main_page")


class AppLogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("management_sys:login")


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy("management_sys:main_page")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


def main_page(request):
    if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
        return redirect("management_sys:login")

    return render(request, 'index.html')
