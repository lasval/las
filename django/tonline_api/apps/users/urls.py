# users/urls.py
from django.urls import include, path
from . import views
from dj_rest_auth.views import LogoutView

urlpatterns = [
    path("current/", views.current, name="current-user"),
    path("login/", views.login, name="login"),
    path(
        "logout/", LogoutView.as_view(), name="logout"
    ),  # 로그아웃은 dj_rest_auth의 logout을 그대로 가져다 사용
    path("registration/", views.registration, name="registration"),
]
