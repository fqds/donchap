from email.policy import default
from statistics import mode
from django.db import models


class Lobby(models.Model):
    lobby_name = models.CharField(max_length=16)
    game_master = models.IntegerField()

    
class LobbyParameter(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='lobby_parameters', on_delete=models.CASCADE)
    parameter_field = models.CharField(max_length=60, null=True)


class LobbyPlayer(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='players', on_delete=models.CASCADE)
    player_id = models.IntegerField()
    
    
class PlayerParameter(models.Model):
    player_identifier = models.ForeignKey(LobbyPlayer, related_name='player_parameters', on_delete=models.CASCADE)
    player_parameter = models.CharField(max_length=1000, default="")
    parameter_name = models.CharField(max_length=15)