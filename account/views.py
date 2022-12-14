from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import AccountAuthenticationForm, RegistrationForm

def entrance_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    context = {}
    return render(request, "account/entrance.html", context)

def login_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    context = {}

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, "account/login.html", context)

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, "account/register.html", context)

def account_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return redirect('entrance')

    context = {}
    return render(request, "account/account.html", context)  

def logout_view(request):
    logout(request)
    return redirect('entrance')