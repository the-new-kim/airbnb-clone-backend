from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("", views.Users.as_view()),
    path("me/", views.Me.as_view()),
    path("change-password/", views.ChangePassword.as_view()),
    path("login/", views.Login.as_view()),  # loign with cookies
    path("logout/", views.Logout.as_view()),
    path("token-login/", obtain_auth_token),  # login with auth Token
    path("jwt-login/", views.JWTLogin.as_view()),  # login with JWT
    path("@<str:username>/", views.PublicUser.as_view()),
]
