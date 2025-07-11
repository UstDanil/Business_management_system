from django.db.models import Avg, Func
from django.db.models.functions import TruncMonth
from django.views import View
from django.views.generic import FormView, DetailView, CreateView
from django.views.generic.edit import ModelFormMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from datetime import date

from .models import Meeting, Task, Team, UserTeam, Evaluation
from .forms import RegisterForm, MeetingForm, TeamForm, TaskForm, EvaluationForm


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


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
            return redirect("management_system:login")
        return render(request, 'index.html')


class MeetingListView(View):
    def get(self, request, *args, **kwargs):
        if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
            return redirect("management_system:login")
        user_meetings = Meeting.objects.filter(meeting_members__user=request.user)
        context = {"meetings": user_meetings}
        return render(request, 'meetings.html', context=context)


class MeetingDetailView(ModelFormMixin, DetailView):
    model = Meeting
    template_name = 'detail/meeting_detail.html'
    form_class = MeetingForm
    success_url = reverse_lazy("management_system:meeting")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class MeetingCreateView(CreateView):
    form_class = MeetingForm
    template_name = 'detail/meeting_detail.html'
    success_url = reverse_lazy("management_system:meeting")


class TaskListView(View):
    def get(self, request, *args, **kwargs):
        if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
            return redirect("management_system:login")
        user_tasks = Task.objects.filter(executor=request.user)
        context = {"tasks": user_tasks}
        return render(request, 'tasks.html', context=context)


class TaskDetailView(ModelFormMixin, DetailView):
    model = Task
    template_name = 'detail/task_detail.html'
    form_class = TaskForm
    success_url = reverse_lazy("management_system:task")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class TaskCreateView(CreateView):
    form_class = TaskForm
    template_name = 'detail/task_detail.html'
    success_url = reverse_lazy("management_system:task")


class TeamListView(View):
    def get(self, request, *args, **kwargs):
        if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
            return redirect("management_system:login")
        user_teams = UserTeam.objects.filter(user=request.user)
        context = {"user_teams": user_teams}
        return render(request, 'teams.html', context=context)


class TeamDetailView(ModelFormMixin, DetailView):
    model = Team
    template_name = 'detail/team_detail.html'
    form_class = TeamForm
    success_url = reverse_lazy("management_system:team")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class TeamCreateView(CreateView):
    form_class = TeamForm
    template_name = 'detail/team_detail.html'
    success_url = reverse_lazy("management_system:team")


class EvaluationListView(View):
    def get(self, request, *args, **kwargs):
        if not hasattr(request, "user") or isinstance(request.user, AnonymousUser):
            return redirect("management_system:login")
        evaluations = Evaluation.objects.filter(user=request.user)
        context = {"evaluations": evaluations}
        today = date.today()
        year_start = date(today.year, 1, 1)
        data = (Evaluation.objects
                .filter(updated_at__range=(year_start, today))
                .annotate(month=DateToChar(TruncMonth('updated_at')))
                .values('month')
                .annotate(avg_mark=Avg('mark')))
        context["average_marks"] = data

        return render(request, 'evaluation.html', context=context)


class EvaluationDetailView(ModelFormMixin, DetailView):
    model = Evaluation
    template_name = 'detail/evaluation_detail.html'
    form_class = EvaluationForm
    success_url = reverse_lazy("management_system:evaluation")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class EvaluationCreateView(CreateView):
    form_class = EvaluationForm
    template_name = 'detail/evaluation_detail.html'
    success_url = reverse_lazy("management_system:evaluation")
