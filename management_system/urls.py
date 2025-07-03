from django.urls import path
from .views import main_page, AppLoginView, AppLogoutView, RegisterView

app_name = "management_sys"

urlpatterns = [
    path('', main_page, name='main_page'),
    path('login/', AppLoginView.as_view(), name='login'),
    path('logout/', AppLogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='registration')
]
