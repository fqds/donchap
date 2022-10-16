from multiprocessing.connection import wait
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from master.math import recount
from master.models import (
    Lobby,
    PlayerItem,
    ItemModifier,
    UpdateParameter,
    UpdateCreateItem,
    UpdateItemName,
    UpdateItemDescription,
    UpdateDeleteItem,
    UpdateCreateItemModifier,
    UpdateItemModifier,
    UpdateDeleteItemModifier,
)


class PlayerConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content):
        command = content.get("command", None)

        try:
            if command == "parameter_update":
                await parameter_update(int(content.get("parameter_id")), content.get("parameter_value"), content.get("lobby_name"), self.scope["user"].pk )
            if command == "create_item":
                await create_item(content.get("lobby_name"), self.scope["user"].pk)
            if command == "update_item_name":
                await update_item_name(content.get("item_id"), content.get("item_name"), content.get("lobby_name"), self.scope["user"].pk)
            if command == "update_item_description":
                await update_item_description(content.get("item_id"), content.get("item_description"), content.get("lobby_name"), self.scope["user"].pk)
            if command == "delete_item":
                await delete_item(content.get("item_id"), content.get("lobby_name"), self.scope["user"].pk)
            if command == "create_item_modifier":
                await create_item_modifier(content.get("item_id"), content.get("lobby_name"), self.scope["user"].pk)
            if command == "update_item_modifier":
                await update_item_modifier(content.get("lobby_name"), self.scope["user"].pk, content.get("item_id"), content.get("modifier_id"), content.get("modifier_value"))
            if command == "delete_item_modifier":
                await delete_item_modifier(content.get("lobby_name"), self.scope["user"].pk, content.get("item_id"), content.get("modifier_id"))
        except Exception as e:
            print(e)

@database_sync_to_async
def parameter_update(parameter_id, parameter_value, lobby_name, user_id):
    lobby = Lobby.objects.get(lobby_name = lobby_name)
    player = lobby.players.get(player_id = user_id)
    parameter = player.parameters.get(parameter_id = parameter_id)
    parameter.parameter_value = parameter_value
    parameter.save()
    update = UpdateParameter(lobby_identifier=lobby, parameter_value=parameter_value, player_id=user_id, parameter_id=parameter.parameter_id)
    update.save()
    data = []
    if lobby.lobby_parameters.get(parameter_id = parameter_id).parameter_stat:
        for i in lobby.lobby_parameters.exclude(parameter_formula = ''):
            if i.parameter_formula.find(lobby.lobby_parameters.all()[parameter_id].parameter_stat) != -1:
                try:
                    parameter = player.parameters.get(parameter_id=i.parameter_id) 
                    formula = i.parameter_formula
                    for j in lobby.lobby_parameters.exclude(parameter_stat = ''):
                        if formula.count(j.parameter_stat) != 0:
                            formula = formula.replace(j.parameter_stat, player.parameters.get(parameter_id=j.parameter_id).parameter_value)
                    parameter.parameter_value = recount(formula) 
                    update = UpdateParameter(lobby_identifier=lobby, parameter_value=parameter.parameter_value, player_id=user_id, parameter_id=i.parameter_id)
                    parameter.save()
                    update.save()
                    data.append([i.parameter_id, parameter.parameter_value])
                except:
                    pass
        
@database_sync_to_async
def create_item(lobby_name, user_id):
    lobby = Lobby.objects.get(lobby_name=lobby_name)
    player = lobby.players.get(player_id=user_id)
    item = PlayerItem(player_identifier=player, item_id=len(player.items.all()))
    update = UpdateCreateItem(lobby_identifier=lobby, player_id=user_id)
    item.save()
    update.save()

@database_sync_to_async
def update_item_name(item_id, item_name, lobby_name, user_id):
    lobby = Lobby.objects.get(lobby_name=lobby_name)
    player = lobby.players.get(player_id=user_id)
    item = player.items.get(item_id=item_id)
    item.item_name = item_name
    update = UpdateItemName(lobby_identifier=lobby, player_id=user_id, item_id=item_id, item_name=item_name)
    item.save()
    update.save()

@database_sync_to_async
def update_item_description(item_id, item_description, lobby_name, user_id):
    lobby = Lobby.objects.get(lobby_name=lobby_name)
    player = lobby.players.get(player_id=user_id)
    item = player.items.get(item_id=item_id)
    item.item_description = item_description
    update = UpdateItemDescription(lobby_identifier=lobby, player_id=user_id, item_id=item_id, item_description=item_description)
    item.save()
    update.save()

@database_sync_to_async
def delete_item(item_id, lobby_name, user_id):
    lobby = Lobby.objects.get(lobby_name=lobby_name)
    player = lobby.players.get(player_id=user_id)
    player.items.get(item_id=item_id).delete()
    for i in player.items.filter(item_id__gt=item_id):
        i.item_id = i.item_id - 1
        i.save()
    update = UpdateDeleteItem(lobby_identifier=lobby, player_id=user_id, item_id=item_id)
    update.save()

@database_sync_to_async
def create_item_modifier(item_id, lobby_name, user_id):
    lobby = Lobby.objects.get(lobby_name=lobby_name)
    player = lobby.players.get(player_id=user_id)
    item = player.items.get(item_id=item_id)
    modifier = ItemModifier(item_identifier=item, modifier_id=len(item.modifiers.all()))
    modifier.save()
    update = UpdateCreateItemModifier(lobby_identifier=lobby, player_id=user_id, item_id=item_id)
    update.save()

@database_sync_to_async
def update_item_modifier(lobby_name, user_id, item_id, modifier_id, modifier_value):
    lobby = Lobby.objects.get(lobby_name=lobby_name)
    player = lobby.players.get(player_id=user_id)
    item = player.items.get(item_id=item_id)
    modifier = item.modifiers.get(modifier_id=modifier_id)
    modifier.modifier_value = modifier_value
    modifier.save()
    update = UpdateItemModifier(lobby_identifier=lobby, player_id=user_id, item_id=item_id, modifier_id=modifier_id, modifier_value=modifier_value)
    update.save()

@database_sync_to_async
def delete_item_modifier(lobby_name, user_id, item_id, modifier_id):
    lobby = Lobby.objects.get(lobby_name=lobby_name)
    player = lobby.players.get(player_id=user_id)
    item = player.items.get(item_id=item_id)
    item.modifiers.get(modifier_id=modifier_id).delete()
    for i in item.modifiers.filter(modifier_id__gt=modifier_id):
        i.modifier_id -= 1
        i.save()
