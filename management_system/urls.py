from django.urls import path
from .views import main_page, AppLoginView, AppLogoutView, RegisterView, MeetingView, TaskView, TeamView, EvaluationView

app_name = "management_system"

urlpatterns = [
    path('', main_page, name='main_page'),
    path('login/', AppLoginView.as_view(), name='login'),
    path('logout/', AppLogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('meeting/', MeetingView.as_view(), name='meeting'),
    path('task/', TaskView.as_view(), name='task'),
    path('team/', TeamView.as_view(), name='team'),
    path('evaluation/', EvaluationView.as_view(), name='evaluation'),

]
