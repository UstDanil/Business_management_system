from django.urls import path
from . import views as app_views

app_name = "management_system"

urlpatterns = [
    path('', app_views.MainPageView.as_view(), name='main_page'),
    path('login/', app_views.AppLoginView.as_view(), name='login'),
    path('logout/', app_views.AppLogoutView.as_view(), name='logout'),
    path('registration/', app_views.RegisterView.as_view(), name='registration'),
    path('meeting/', app_views.MeetingListView.as_view(), name='meeting'),
    path('meeting/create/', app_views.MeetingCreateView.as_view(), name='meeting_create'),
    path('meeting/<uuid:pk>/', app_views.MeetingDetailView.as_view(), name='meeting_detail'),
    path('task/', app_views.TaskListView.as_view(), name='task'),
    path('task/create/', app_views.TaskCreateView.as_view(), name='task_create'),
    path('task/<uuid:pk>/', app_views.TaskDetailView.as_view(), name='task_detail'),
    path('team/', app_views.TeamListView.as_view(), name='team'),
    path('team/create/', app_views.TeamCreateView.as_view(), name='team_create'),
    path('team/<uuid:pk>/', app_views.TeamDetailView.as_view(), name='team_detail'),
    path('evaluation/', app_views.EvaluationListView.as_view(), name='evaluation'),
    path('evaluation/create/', app_views.EvaluationCreateView.as_view(), name='evaluation_create'),
    path('evaluation/<uuid:pk>/', app_views.EvaluationDetailView.as_view(), name='evaluation_detail'),
]
