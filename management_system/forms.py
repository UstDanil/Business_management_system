from django.contrib.auth.forms import UserCreationForm
from .models import User, Meeting, Team, Task, Evaluation, UserTeam, UserMeeting
from django import forms


class CheckReadOnlyMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop('readonly', False)
        super().__init__(*args, **kwargs)
        if readonly:
            for field_name, field in self.fields.items():
                field.widget.attrs['disabled'] = 'disabled'


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic']


class MeetingForm(CheckReadOnlyMixin):
    class Meta:
        model = Meeting
        fields = ["name", "comments", "day", "time"]


class MeetingMemberForm(CheckReadOnlyMixin):
    class Meta:
        model = UserMeeting
        exclude = ()


MeetingMemberFormSet = forms.inlineformset_factory(Meeting, UserMeeting, form=MeetingMemberForm)


class TeamForm(CheckReadOnlyMixin):
    class Meta:
        model = Team
        fields = ["name"]


class TeamMemberForm(CheckReadOnlyMixin):
    class Meta:
        model = UserTeam
        exclude = ()


TeamMemberFormSet = forms.inlineformset_factory(Team, UserTeam, form=TeamMemberForm)


class TaskForm(CheckReadOnlyMixin):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "comments",
                  "deadline", "executor"]


class EvaluationForm(CheckReadOnlyMixin):
    class Meta:
        model = Evaluation
        fields = ["user", "task", "mark"]
