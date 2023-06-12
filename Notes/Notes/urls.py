"""Notes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# from main.views import Notes_view, Note_view, Note_create_view, Note_delete_view
from main.views import (
    home_view,
    create_view,
    edit_view,
    delete_view,
    empty_view,
    search_view,
)
from accounts.views import register_view, login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="index"),
    path("create/", create_view, name="create"),
    path("notes/<int:id>/", edit_view, name="edit"),
    path("delete/<int:id>/", delete_view, name="delete"),
    path("empty/", empty_view, name="empty"),
    path("search/", search_view, name="search"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # path('<int:pk>/', Note_view.as_view()),
    # path('create/', Note_create_view.as_view()),
    # path('delete/', Note_delete_view.as_view()),
]
