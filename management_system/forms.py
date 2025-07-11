from django.contrib.auth.forms import UserCreationForm
from .models import User, Meeting, Team, Task, Evaluation
from django import forms


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic']


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ["name", "comments", "day", "time"]


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "comments",
                  "deadline", "executor"]


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["user", "task", "mark"]
