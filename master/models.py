from django.db import models


class Lobby(models.Model):
    lobby_name = models.CharField(max_length=16)
    game_master = models.IntegerField()


class LobbyParameter(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='lobby_parameters', on_delete=models.CASCADE)
    parameter_name = models.CharField(max_length=20, null=True)
    parameter_stat = models.CharField(max_length=10, null=True)
    parameter_formula = models.CharField(max_length=30, null=True)
    parameter_id = models.IntegerField()


class LobbyPlayer(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='players', on_delete=models.CASCADE)
    player_id = models.IntegerField()
    
    
class PlayerParameter(models.Model):
    player_identifier = models.ForeignKey(LobbyPlayer, related_name='parameters', on_delete=models.CASCADE)
    parameter_value = models.CharField(max_length=20, default="")
    parameter_id = models.IntegerField()
    class Meta():
        ordering = ['pk']

class PlayerItem(models.Model):
    player_identifier = models.ForeignKey(LobbyPlayer, related_name='items', on_delete=models.CASCADE)
    item_id = models.IntegerField()
    item_name = models.CharField(max_length=20, default="")
    item_description = models.CharField(max_length=1000, default="")
    class Meta():
        ordering = ['pk']

class ItemModifier(models.Model):
    item_identifier = models.ForeignKey(PlayerItem, related_name='stats', on_delete=models.CASCADE)
    modifier_stat = models.CharField(max_length=10, null=True)
    modifier_value = models.CharField(max_length=10, null=True)
    class Meta():
        ordering = ['pk']

class UpdatedParameter(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='updated_parameters', on_delete=models.CASCADE)
    parameter_value = models.CharField(max_length=20)
    parameter_id = models.IntegerField()
    player_id = models.IntegerField()