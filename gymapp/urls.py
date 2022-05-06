
from django.urls import path

from . import views


urlpatterns =[
 path("", views.index, name="index"),
 path("reserv", views.reserv, name="reserv"),
 path("login", views.login_view, name="login"),
 path("logout", views.logout_view, name="logout"),
 path("register", views.register, name="register"),
 path("api", views.api, name="api"),
 path("comment/<int:user_id>", views.comment, name="comment"),
 path("questions", views.questions, name="questions"),
 path("enrolled", views.enrolled, name="enrolled")
]