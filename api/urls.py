from django.urls import path

from . import api

urlpatterns = [
    path("advert/", api.Adverts.Index.to_route, name="adverts"),
    path("advert/<int:pk>", api.Adverts.Advert.to_route, name="advert"),
    path("advert/<int:pk>/apply", api.Adverts.Apply.to_route, name="advert"),
    path("advert/<int:pk>/apps", api.Adverts.Apps.to_route, name="apps"),
    path("user/", api.Users.Index.to_route, name="users"),
    path("user/<int:pk>", api.Users.User.to_route, name="user"),
    path("user/authenticate", api.Users.Authenticate.to_route, name="user_authenticate"),
    path("user/register", api.Users.Register.to_route, name="user_register"),

]

