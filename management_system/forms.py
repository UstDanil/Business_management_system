from django.contrib.auth.forms import UserCreationForm
from .models import User, Meeting, Team, Task, Evaluation, UserTeam, UserMeeting
from django import forms


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic']


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ["name", "comments", "day", "time"]


class MeetingMemberForm(forms.ModelForm):
    class Meta:
        model = UserMeeting
        exclude = ()


MeetingMemberFormSet = forms.inlineformset_factory(Meeting, UserMeeting, form=MeetingMemberForm)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name"]


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = UserTeam
        exclude = ()


TeamMemberFormSet = forms.inlineformset_factory(Team, UserTeam, form=TeamMemberForm)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "comments",
                  "deadline", "executor"]


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["user", "task", "mark"]
