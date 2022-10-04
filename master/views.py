from django.shortcuts import render, redirect

from master.forms import CreateLobbyForm
from master.models import (
    Lobby,
    LobbyParameter,
    LobbyPlayer,
    PlayerParameter,
)

def create_lobby_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return redirect('entrance')
    

    if request.POST:
        form = CreateLobbyForm(request.POST)

        lobby_name = request.POST['lobby_name']
        raw_content = request.POST['content']
        try:
            lobby = Lobby.objects.get(lobby_name = lobby_name)
        except Lobby.DoesNotExist:
            lobby = Lobby(lobby_name=lobby_name,game_master=user.pk)
            lobby.save()
            for i in raw_content.split('\r\n'):
                lobby_parameter = LobbyParameter(lobby_identifier=lobby, parameter_field=i)
                lobby_parameter.save()
            return redirect('lobby:view', lobby_name=lobby_name)
    else:
        form = CreateLobbyForm()
    context = {'form': form}
    return render(request, "master/create_lobby.html", context)

def lobby_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return redirect('entrance')
    context = {}
    
    lobby_name = kwargs.get('lobby_name')

    lobby = Lobby.objects.get(lobby_name = lobby_name)
    content = []
    for i in lobby.lobby_parameters.all():
        content.append(i.parameter_field.split())

    if user.pk == lobby.game_master:
        context['is_master'] = True
    else:
        context['is_master'] = False
        flag = False
        for p in lobby.players.all():
            if p.player_id == user.pk:
                flag = True
        if not flag:
            player = LobbyPlayer(lobby_identifier=lobby, player_id=user.pk)
            player.save()
            for i in lobby.lobby_parameters.all():
                player_parameter = PlayerParameter(player_identifier=player)
                player_parameter.save()


    context['content']=content
    return render(request, "master/lobby.html", context)

def connect_lobby_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('entrance')
    context = {}

    if request.POST:
        lobby_name = request.POST['lobby_name']
        if Lobby.objects.get(lobby_name = lobby_name):
            return redirect('lobby:view', lobby_name=lobby_name)
        
    return render(request, "master/connect_lobby.html", context)