from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from master.math import recount
from master.models import (
    Lobby,
    LobbyParameter,
    LobbyPlayer,
    PlayerParameter,
    UpdatedParameter,
)


class PlayerConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content):
        command = content.get("command", None)

        try:
            if command == "parameter_update":
                data = await parameter_update(int(content.get("parameter_id")), content.get("parameter_value"), content.get("lobby_name"), self.scope["user"].pk )

                await self.send_json(
                    {
                        "update_stats": data,
                    },)
        except Exception as e:
            print(e)

@database_sync_to_async
def parameter_update(parameter_id, parameter_value, lobby_name, user_id):
    lobby = Lobby.objects.get(lobby_name = lobby_name)
    player = lobby.players.get(player_id = user_id)
    parameter = player.parameters.get(parameter_id = parameter_id)
    parameter.parameter_value = parameter_value
    parameter.save()
    update = UpdatedParameter(lobby_identifier=lobby, parameter_value=parameter_value, player_id=user_id, parameter_id=parameter.parameter_id)
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
                    update = UpdatedParameter(lobby_identifier=lobby, parameter_value=parameter.parameter_value, player_id=user_id, parameter_id=i.parameter_id)
                    parameter.save()
                    update.save()
                    data.append([i.parameter_id, parameter.parameter_value])
                except:
                    pass
    return data
        


class MasterConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content):
        command = content.get("command", None)

        try:
            if command == "get_update":
                data = await get_update(content.get("lobby_name"))

                await self.send_json(
                    {
                        "update_data": data,
                    },
                )
            if command == "get_data":
                data = await get_data(content.get("lobby_name"))
                await self.send_json(
                    {
                        "receive_data": data,
                    },
                )

        except Exception as e:
            print(e)

            

@database_sync_to_async
def get_update(lobby_name):
    lobby = Lobby.objects.get(lobby_name = lobby_name)
    data = []
    if lobby.updated_parameters.all():
        for i in lobby.updated_parameters.all():
            data.append([i.player_id, i.parameter_id, i.parameter_value])
    lobby.updated_parameters.all().delete()
    return data

@database_sync_to_async
def get_data(lobby_name):
    lobby = Lobby.objects.get(lobby_name = lobby_name)

    content = []
    for i in lobby.players.all():
        content.append([i.pk,[]])
        for i in i.parameters.all():
            content[-1][1].append(i.parameter_value)
    lobby.updated_parameters.all().delete()
    return content
