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
        if parameter.parameter_formula: l=False
        else: l=True

        content.append([i, 
                        parameter.parameter_name, 
                        player.parameters.all()[i].parameter_value,
                        l])

    inventory = []
    for i in player.items.all():
        inventory.append([i.item_id, i.item_name, i.item_description])
    
    context['inventory'] = inventory
    context['lobby_name'] = lobby_name
    context['content'] = content
    return render(request, "player/lobby.html", context)