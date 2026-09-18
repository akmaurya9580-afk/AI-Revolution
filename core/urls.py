from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("analyze/", views.analyze_text, name="analyze_text"),

    path("contact/", views.contact, name="contact"),

    path("api/chat/", views.chat_api, name="chat_api"),

    path("register/", views.register, name="register"),

    path("login/", views.login_view, name="login"),

    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "change-password/",
        views.change_password,
        name="change_password"
    ),

    path(
        "edit-profile/",
        views.edit_profile,
        name="edit_profile"
    ),
]