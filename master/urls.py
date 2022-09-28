from django.urls import path

from master.views import (
    lobby_view
)

app_name = 'lobby'

urlpatterns = [
    path('<lobby_name>/', lobby_view, name="view"),
]
