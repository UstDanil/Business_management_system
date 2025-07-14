from django.contrib import admin
from .models import User, Team, Task, Meeting, Evaluation, UserTeam, UserMeeting


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ["email", "first_name", "last_name", "patronymic", "role"]
    # list_display = ["email", "first_name", "last_name", "patronymic", "role"]


admin.site.register(Team)
admin.site.register(Task)
admin.site.register(Meeting)
admin.site.register(Evaluation)
admin.site.register(UserTeam)
admin.site.register(UserMeeting)
