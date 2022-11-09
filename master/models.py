from email.policy import default
from django.db import models
from django.forms import IntegerField


class Lobby(models.Model):
    lobby_name = models.CharField(max_length=16)
    game_master = models.IntegerField()


class LobbyParameter(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='lobby_parameters', on_delete=models.CASCADE)
    parameter_name = models.CharField(max_length=30)
    parameter_stat = models.CharField(max_length=20, null=True)
    parameter_formula = models.CharField(max_length=70, null=True)
    parameter_id = models.IntegerField()


class LobbyPlayer(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='players', on_delete=models.CASCADE)
    player_id = models.IntegerField()
    
    
class PlayerParameter(models.Model):
    player_identifier = models.ForeignKey(LobbyPlayer, related_name='parameters', on_delete=models.CASCADE)
    parameter_value = models.CharField(max_length=20, default="")
    parameter_modifier = models.IntegerField(default=0)
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

class UpdateItemDescription(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='update_item_description', on_delete=models.CASCADE)
    player_id = models.IntegerField()
    item_id = models.IntegerField()
    item_description = models.CharField(max_length=1000)

class UpdateItemName(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='update_item_names', on_delete=models.CASCADE)
    player_id = models.IntegerField()
    item_id = models.IntegerField()
    item_name = models.CharField(max_length=1000)

class UpdateCreateItem(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='update_create_items', on_delete=models.CASCADE)
    player_id = models.IntegerField()

class UpdateDeleteItem(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='update_delete_items', on_delete=models.CASCADE)
    player_id = models.IntegerField()
    item_id = models.IntegerField()

class UpdateParameter(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='update_parameters', on_delete=models.CASCADE)
    parameter_value = models.CharField(max_length=20)
    parameter_id = models.IntegerField()
    player_id = models.IntegerField()

class ItemModifier(models.Model):
    item_identifier = models.ForeignKey(PlayerItem, related_name='modifiers', on_delete=models.CASCADE)
    modifier_id = models.IntegerField()
    modifier_value = models.CharField(max_length=40, default="")
    class Meta():
        ordering = ['pk']

class UpdateCreateItemModifier(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='update_create_item_modifier', on_delete=models.CASCADE)
    player_id = models.IntegerField()
    item_id = models.IntegerField()
    
class UpdateItemModifier(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='update_item_modifier', on_delete=models.CASCADE)
    player_id = models.IntegerField()    
    item_id = models.IntegerField()
    modifier_id = models.IntegerField()
    modifier_value = models.CharField(max_length=40)

class UpdateDeleteItemModifier(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='update_delete_item_modifier', on_delete=models.CASCADE)
    player_id = models.IntegerField()
    item_id = models.IntegerField()
    modifier_id = models.IntegerField()


class LobbyParameterBar(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='lobby_parameters_bars', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    max_value_name = models.CharField(max_length=30)
    max_value_formula = models.CharField(max_length=70)
    negative_value_formula = models.CharField(max_length=70)
    color = models.CharField(max_length=15)


class PlayerParameterBar(models.Model):
    player_identifier = models.ForeignKey(LobbyPlayer, related_name='bars', on_delete=models.CASCADE)
    max_value = models.CharField(max_length=20, default="")
    negative_value = models.CharField(max_length=20, default="")
    bar_id = models.IntegerField()
    class Meta():
        ordering = ['pk']


class UpdateParameterBar(models.Model):
    lobby_identifier = models.ForeignKey(Lobby, related_name='update_bars', on_delete=models.CASCADE)
    max_value = models.IntegerField()
    negative_value = models.IntegerField()
    bar_id = models.IntegerField()
    player_id = models.IntegerField()