from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
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
                await parameter_update(content.get("parameter_id"), content.get("parameter_value"), content.get("lobby_name"), self.scope["user"].pk )

        except Exception as e:
            print(e)

@database_sync_to_async
def parameter_update(parameter_id, parameter_value, lobby_name, user_id):
    lobby = Lobby.objects.get(lobby_name = lobby_name)
    player = lobby.players.get(player_id = user_id)
    parameter = player.player_parameters.get(parameter_id = parameter_id)
    parameter.player_parameter = parameter_value
    parameter.save()
    update = UpdatedParameter(lobby_identifier=lobby, parameter=parameter_value, player_id=user_id, parameter_id=parameter.parameter_id)
    update.save()



class MasterConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content):
        command = content.get("command", None)

        try:
            if command == "get_update":
                data = await get_update(content.get("lobby_name"))

                await self.send_json(
                    {
                        "update_data": True,
                        "data_to_update": data
                    },
                )
            if command == "get_data":
                data = await get_data(content.get("lobby_name"))
                await self.send_json(
                    {
                        "receive_data": True,
                        "content": data,
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
            data.append([i.player_id, i.parameter_id, i.parameter])
    lobby.updated_parameters.all().delete()
    return data

@database_sync_to_async
def get_data(lobby_name):
    lobby = Lobby.objects.get(lobby_name = lobby_name)

    content = []
    for i in lobby.players.all():
        content.append([i.pk,[]])
        for i in i.player_parameters.all():
            content[-1][1].append(i.player_parameter)
    lobby.updated_parameters.all().delete()
    return content