from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse


def register_view(request):
    if request.user.is_anonymous:
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful, please log in")
            return redirect('login')
        context = {"form": form}
        return render(request, "accounts/register.html", context)
    else:
        messages.error(request, "Can't register now, try logging out first")
        return redirect('index')


def login_view(request):
    if request.user.is_anonymous:
        if request.method == "GET":
            form = AuthenticationForm(request)
            context = {"form": form}
            return render(request, "accounts/login.html", context)
        elif request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Invalid login or password")
                return redirect('login')
    else:
        messages.error(request, "Can't login now, try logging out first")
        return redirect('index')


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]

    status_code = 200


@login_required(redirect_field_name=None)
def logout_view(request):
    if request.META.get('HTTP_HX_REQUEST'):
        logout(request)
        messages.success(request, "Logged out successfully")
        return HTTPResponseHXRedirect(redirect_to=reverse("login"))
    if request.method == "GET":
        return render(request, "accounts/logout.html")
    elif request.method == "POST":
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('index')

