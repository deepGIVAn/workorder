from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register_client/", views.register_client, name="register_client"),
    path("register_admin/", views.register_admin, name="register_admin"),
]
