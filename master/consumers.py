from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from master.models import (
    Lobby,
    LobbyParameter,
    LobbyPlayer,
    PlayerParameter,
)


class PlayerConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content):
        command = content.get("command", None)

        try:
            if command == "parameter_update":
                await parameter_update(content.get("parameter_name"), content.get("parameter_value"), content.get("lobby_name"), self.scope["user"].pk )

        except Exception as e:
            print(e)

@database_sync_to_async
def parameter_update(parameter_name, parameter_value, lobby_name, user_id):
    print(parameter_name, parameter_value, lobby_name, user_id)
    lobby = Lobby.objects.get(lobby_name = lobby_name)
    player = lobby.players.get(player_id = user_id)
    parameter = player.player_parameters.get(parameter_name = parameter_name)
    parameter.player_parameter = parameter_value
    parameter.save()

