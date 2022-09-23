from django.shortcuts import render

def entrance_view(request):
    context = {}
    return render(request, "account/entrance.html", context)

def login_view(request):
    context = {}
    return render(request, "account/login.html", context)

def register_view(request):
    context = {}
    return render(request, "account/register.html", context)