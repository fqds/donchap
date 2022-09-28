from django.shortcuts import render, redirect

from master.forms import CreateLobbyForm
from master.models import Lobby, LobbyParameter
from account.models import Account

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
            print('a')
        except Lobby.DoesNotExist:
            lobby = Lobby(lobby_name=lobby_name,game_master=user.pk)
            lobby.save()
            content = []
            temp = []
            for i in raw_content.split():
                for j in ['a','b','c','d']:
                    if i==j and temp:
                        content.append(temp)
                        temp = []
                temp.append(i)
            content.append(temp)
            for i in content:
                temp = ' '.join(i)
                lobby_parameter = LobbyParameter(parameter_field=temp, lobby_identifier=lobby)
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

    if user.pk == int(lobby.game_master):
        context['is_master'] = True
    else:
        context['is_master'] = False
    context['content']=content
    print(context)
    return render(request, "master/lobby.html", context)