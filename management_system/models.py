import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, Base):
    ROLES = {
        'worker': 'worker',
        'manager': 'manager',
        'admin': 'admin',
    }
    email = models.EmailField(verbose_name=_("E-mail"))
    password = models.CharField(max_length=255, verbose_name=_("Пароль"))
    first_name = models.CharField(max_length=30, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=30, verbose_name=_("Фамилия"))
    patronymic = models.CharField(max_length=30, verbose_name=_("Отчество"), null=True, blank=True)
    role = models.CharField(max_length=7, choices=ROLES, verbose_name=_("Роль"))

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name


class Team(Base):
    name = models.CharField(max_length=255, verbose_name=_("Название команды"))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams_created",
                              verbose_name=_("Руководитель команды"), null=False)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.name


class Task(Base):
    STATUS = {
        'waiting': 'waiting',
        'closed': 'closed',
        'in_progress': 'in_progress',
    }
    name = models.CharField(max_length=255, verbose_name=_("Название задачи"))
    description = models.CharField(max_length=255, verbose_name=_("Описание"))
    status = models.CharField(max_length=11, choices=STATUS, verbose_name=_("Статус задачи"))
    comments = models.CharField(max_length=255, verbose_name=_("Комментарии к задаче"), null=True, blank=True)
    deadline = models.DateTimeField(verbose_name=_("Крайний срок исполнения"))
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_executed",
                                 verbose_name=_("Исполнитель"), null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_created",
                                verbose_name=_("Создал задачу"), null=False)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name


class UserTeam(Base):
    POSITION = {
        'worker': 'worker',
        'manager': 'manager',
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_teams",
                             verbose_name=_("Член команды"), null=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_members",
                             verbose_name=_("Название команды"), null=False)
    position = models.CharField(max_length=7, choices=POSITION, verbose_name=_("Роль в команде"))

    class Meta:
        verbose_name = 'Член команды'
        verbose_name_plural = 'Члены команд'

    def __str__(self):
        return f"Участники: {self.user}, Название команды: {self.team}"


class Meeting(Base):
    name = models.CharField(max_length=255, verbose_name=_("Название встречи"))
    comments = models.TextField(verbose_name=_("Комментарии"))
    day = models.DateField(max_length=255, verbose_name=_("День встречи"))
    time = models.TimeField(max_length=255, verbose_name=_("Время встречи"))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meetings_created",
                                verbose_name=_("Создал встречу"), null=False)

    class Meta:
        verbose_name = 'Встреча'
        verbose_name_plural = 'Встречи'

    def __str__(self):
        return self.name


class UserMeeting(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_meetings",
                             verbose_name=_("Участник встречи"), null=False)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="meeting_members",
                                verbose_name=_("Название встречи"), null=False)

    class Meta:
        verbose_name = 'Встреча пользователя'
        verbose_name_plural = 'Встречи пользователей'

    def __str__(self):
        return f"Имя участника: {self.user} Название встречи: {self.meeting}"


class Evaluation(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="worker",
                             verbose_name=_("Работник"), null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_name",
                             verbose_name=_("Задача"), null=True)
    mark = models.IntegerField(validators=(MinValueValidator(1), MaxValueValidator(5)),
                               verbose_name=_("Оценка"), null=True)

    class Meta:
        verbose_name = 'Оценка задачи'
        verbose_name_plural = 'Оценки задач'

    def __str__(self):
        return f"{self.user}, {self.task}"
