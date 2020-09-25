
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("following", views.following, name="following"),
    path("profile/follow/<str:username>", views.follow_user, name="follow"),
    path("profile/unfollow/<str:username>", views.unfollow_user, name="unfollow"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("like/<int:post_id>", views.like_post, name="like"),
    path("edit/<int:post_id>", views.edit_post, name="edit")
]
