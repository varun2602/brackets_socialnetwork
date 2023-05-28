
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_post', views.create_post, name = "create_post"),
    path('<str:name>/profile_page', views.profile_page, name = "profile_page"),
    path('test', views.test, name = "test"),
    path('<str:name>/follow', views.follow, name = "follow"),
    path('<str:user_clicked>/<str:user_active>/unfollow', views.unfollow, name = "unfollow"),
    path('<str:user_clicked>/followers', views.followers, name = "followers"),
    path("<str:user_clicked>/following", views.following, name = "following"),
    path('following_page', views.following_page, name = "following_page"),
    path('edit_post/<int:post_id>', views.edit_post, name = "edit_post")


]
