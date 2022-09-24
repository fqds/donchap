"""donchap URL Configuration

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
from account.views import (
    entrance_view,
    login_view,
    register_view,
    account_view,
    logout_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('entrance', entrance_view, name="entrance"),
    path('login', login_view, name="login"),
    path('register', register_view, name="register"),
    path('', account_view, name="home"),
    path('logout', logout_view, name="logout"),
]
