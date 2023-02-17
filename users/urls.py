from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("", views.Users.as_view()),
    path("me/", views.Me.as_view()),
    path("change-password/", views.ChangePassword.as_view()),
    path("login/", views.Login.as_view()),
    path("logout/", views.Logout.as_view()),
    path("token-login/", obtain_auth_token),
    path("@<str:username>/", views.PublicUser.as_view()),
]
