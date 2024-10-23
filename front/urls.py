from django.urls import path
from django.shortcuts import render



def view(page): return lambda request: render(request, template_name=page)

urlpatterns = [
    path("", view('index.html'), name="index"),
    path("apply", view('apply.html'), name="apply"),
    path("signin", view('signin.html'), name="signin"),
    path("signup", view('signup.html'), name="signup"),
    path("panel", view('panel.html'), name="panel"),
    path("edit", view('edit.html'), name="edit"),
]