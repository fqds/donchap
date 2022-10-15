from django.urls import path

from master.views import (
    lobby_master_view
)

app_name = 'lobby'

urlpatterns = [
    path('<lobby_name>/', lobby_master_view, name="master_view"),
]
