from django.shortcuts import render, redirect
from master.models import (
    Lobby,
    LobbyPlayer,
    PlayerParameter,
)

def lobby_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return redirect('entrance')
    context = {}
    
    lobby_name = kwargs.get('lobby_name')
    lobby = Lobby.objects.get(lobby_name = lobby_name)


    content = []
    if user.pk == lobby.game_master:
        return redirect('lobby_master:view', lobby_name=lobby_name) 
    try:
        player = lobby.players.get(player_id = user.pk)
    except:
        player = LobbyPlayer(lobby_identifier=lobby, player_id=user.pk)
        player.save()
        for i in range(len(lobby.lobby_parameters.all())):
            parameter_value = PlayerParameter(player_identifier=player, parameter_id=i)
            parameter_value.save()


    for i in range(len(lobby.lobby_parameters.all())):
        parameter = lobby.lobby_parameters.all()[i]
        if not parameter.parameter_formula: 
            content.append([i, 
                    parameter.parameter_name, 
                    player.parameters.all()[i].parameter_value])

    inventory = []
    for item in player.items.all():
        inventory.append([item.item_id, item.item_name, item.item_description,[]])
        for modifier in item.modifiers.all():
            inventory[-1][3].append([modifier.modifier_id, modifier.modifier_value])
    
    context['inventory'] = inventory
    context['lobby_name'] = lobby_name
    context['content'] = content
    return render(request, "player/lobby.html", context)