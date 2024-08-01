"""URLs for the users app."""

from django.urls import path

from accounts.rest.views.users import UserCreateView, UserListView, LoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("registration/", UserCreateView.as_view(), name="user-list-create"),
    path("", UserListView.as_view(), name="user-list"),
]