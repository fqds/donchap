from django.urls import path

from player.views import (
    lobby_view
)

app_name = 'lobby'

urlpatterns = [
    path('<lobby_name>/', lobby_view, name="master_view"),
]
