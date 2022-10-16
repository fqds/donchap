from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from master.models import Lobby


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

        except Exception as e:
            print(e)

            

@database_sync_to_async
def get_update(lobby_name):
    lobby = Lobby.objects.get(lobby_name = lobby_name)
    data = [[],[],[],[],[],[],[],[]]
    if lobby.update_parameters.all():
        for i in lobby.update_parameters.all():
            data[0].append([i.player_id, i.parameter_id, i.parameter_value])
    lobby.update_parameters.all().delete()

    if lobby.update_create_items.all():
        for i in lobby.update_create_items.all():
            data[1].append([i.player_id])
    lobby.update_create_items.all().delete()

    if lobby.update_item_names.all():
        for i in lobby.update_item_names.all():
            data[2].append([i.player_id, i.item_id, i.item_name])
    lobby.update_item_names.all().delete()

    if lobby.update_item_description.all():
        for i in lobby.update_item_description.all():
            data[3].append([i.player_id, i.item_id, i.item_description])
    lobby.update_item_description.all().delete()

    if lobby.update_delete_items.all():
        for i in lobby.update_delete_items.all():
            data[4].append([i.player_id, i.item_id])
    lobby.update_delete_items.all().delete()

    if lobby.update_create_item_modifier.all():
        for i in lobby.update_create_item_modifier.all():
            data[5].append([i.player_id, i.item_id])
    lobby.update_create_item_modifier.all().delete()

    if lobby.update_item_modifier.all():
        for i in lobby.update_item_modifier.all():
            data[6].append([i.player_id, i.item_id, i.modifier_id, i.modifier_value])
    lobby.update_item_modifier.all().delete()

    if lobby.update_delete_item_modifier.all():
        for i in lobby.update_delete_item_modifier.all():
            data[7].append([i.player_id, i.item_id, i.modifier_id])
    lobby.update_delete_item_modifier.all().delete()
    return data

