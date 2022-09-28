from statistics import mode
from django.db import models

class LobbyManager(models.Model):
    def create_lobby(self, lobby_name, content):
        Lobby(lobby_name=lobby_name)
        print(content.split())

class Lobby(models.Model):
    lobby_name = models.CharField(max_length=16)
    game_master = models.CharField(max_length=5)

    
class LobbyParameter(models.Model):
    parameter_field = models.CharField(max_length=60, null=True)
    lobby_identifier = models.ForeignKey(Lobby, related_name='lobby_parameters', on_delete=models.CASCADE)
