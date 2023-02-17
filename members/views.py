from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm


def register_client(request):
    if request.user.is_superuser:
        return redirect("admin_home")
    elif request.user.is_authenticated:
        return redirect("client_home")
    else:
        if request.method == "POST":
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("Registration successful.."))
                return redirect("login")
        else:
            form = RegisterUserForm()
        return render(request, "auth/register_client.html", {"form": form})


def register_admin(request):
    if request.user.is_superuser:
        return redirect("admin_home")
    elif request.user.is_authenticated:
        return redirect("client_home")
    else:
        if request.method == "POST":
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                key = request.POST.get('key')
                if key == '76fb3134091e9b3':                       # with out private key you are not allowed to register as admin
                    user = form.save(commit=False)
                    user.is_staff = True  # Set the is_staff attribute to True
                    # user.set_password(form.cleaned_data['password'])
                    user.is_superuser = True
                    user.save()
                    messages.success(request, ("Registration successful.."))
                    return redirect("login")
                else:
                    messages.success(request,("Please Enter the right Key to Register as the Admin !!"))
                    form = RegisterUserForm()
                    return render(request, "auth/register_admin.html", {"form": form})                    
        else:
            # form = UserCreationForm()
            form = RegisterUserForm()
        return render(request, "auth/register_admin.html", {"form": form})


def login_user(request):
    if request.user.is_superuser:
        return redirect("admin_home")
    elif request.user.is_authenticated:
        return redirect("client_home")
    else:
        if request.method == "POST":
            un = request.POST["username"]
            pswd = request.POST["password"]
            user = authenticate(request, username=un, password=pswd)
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    messages.success(request, ("Welcome! Admins"))
                    return redirect("admin_home")
                else:
                    messages.success(
                        request, ("A great Welcome you to the Work Orders Managemet System..")
                    )
                    return redirect("client_home")
            else:
                # Return an invalid login error..
                messages.success(
                    request, ("There were some error logining in..Please try again ..")
                )
                return redirect("login")
        else:
            return render(request, "auth/login.html", {})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, ("You were logged out!!"))
    return redirect("login")
