from django.db.models import Avg, Func, F
from django.db.models.functions import ExtractMonth, TruncMonth
from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from datetime import datetime, date, timedelta

from .models import User, Meeting, Task, Team, UserTeam, Evaluation
from .forms import RegisterForm


class DateToChar(Func):
    function = 'TO_CHAR'
    template = "%(function)s(%(expressions)s, 'YYYY-MM')"


class AppLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy("management_system:main_page")


class AppLogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("management_system:login")


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy("management_system:main_page")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


def main_page(request):
    if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
        return redirect("management_system:login")

    return render(request, 'index.html')


class MeetingView(View):
    def get(self, request, *args, **kwargs):
        if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
            return redirect("management_system:login")
        user_id = request.user.id
        user_meetings = Meeting.objects.filter(meeting_members__user=request.user)
        context = {"meetings": user_meetings}
        return render(request, 'meetings.html', context=context)


class TaskView(View):
    def get(self, request, *args, **kwargs):
        if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
            return redirect("management_system:login")
        user_id = request.user.id
        user_tasks = Task.objects.filter(executor=request.user)
        context = {"tasks": user_tasks}
        return render(request, 'tasks.html', context=context)


class TeamView(View):
    def get(self, request, *args, **kwargs):
        if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
            return redirect("management_system:login")
        user_teams = UserTeam.objects.filter(user=request.user)
        context = {"user_teams": user_teams}
        return render(request, 'teams.html', context=context)


class EvaluationView(View):
    def get(self, request, *args, **kwargs):
        if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
            return redirect("management_system:login")
        user_evaluation = Evaluation.objects.filter(user=request.user)
        context = {"user_evaluations": user_evaluation}
        today = date.today()
        year_start = date(today.year, 1, 1)
        data = (Evaluation.objects
                .filter(updated_at__range=(year_start, today))
                .annotate(month=DateToChar(TruncMonth('updated_at')))
                .values('month')
                .annotate(avg_mark=Avg('mark')))
        context["average_marks"] = data

        return render(request, 'evaluation.html', context=context)
