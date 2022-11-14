from django.shortcuts import render, redirect

from master.forms import CreateLobbyForm
from master.models import (
    Lobby,
    LobbyParameter,
    LobbyParameterBar
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
            for parameter in raw_content.split('\r\n'):
                i = parameter.split()
                if len(i) == 5: 
                    lobby_bar = LobbyParameterBar(lobby_identifier=lobby,
                                                  name=i[0],
                                                  max_value_name=i[1],
                                                  max_value_formula=i[2],
                                                  negative_value_formula=i[3],
                                                  color=i[4],
                                                  bar_id=len(lobby.lobby_parameter_bars.all()))
                    lobby_bar.save()
                else:
                    if len(i) == 3: 
                        stat = i[1]
                        formula = i[2]
                    elif len(i) == 2:
                        stat = i[1]
                        formula = ''
                    else: 
                        stat = ''
                        formula = ''
                    lobby_parameter = LobbyParameter(lobby_identifier=lobby,
                                                     parameter_name=i[0],
                                                     parameter_stat=stat,
                                                     parameter_formula=formula,
                                                     parameter_id=len(lobby.lobby_parameters.all()),)
                    lobby_parameter.save()
            return redirect('lobby_master:view', lobby_name=lobby_name)
    else:
        form = CreateLobbyForm()
    context = {'form': form}
    return render(request, "master/create_lobby.html", context)



def lobby_master_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return redirect('entrance')
    context = {}
    
    lobby_name = kwargs.get('lobby_name')
    lobby = Lobby.objects.get(lobby_name = lobby_name)


    if user.pk != lobby.game_master:
        return redirect('lobby:view', lobby_name=lobby_name)

    parameters = []
    for i in lobby.lobby_parameter_bars.all():
        parameters.append(i.name)
    for i in lobby.lobby_parameters.all():
        parameters.append(i.parameter_name)

    players = []
    for i in lobby.players.all(): players.append(i.player_id)

    content = []
    for i in lobby.players.all():
        content.append([[],[],[]])
        for j in i.parameters.all():
            try: content[-1][0].append(int(j.parameter_value) + j.parameter_modifier)
            except: content[-1][0].append(j.parameter_value)
        for j in i.items.all():
            content[-1][1].append([j.item_name, j.item_description, []])
            for k in j.modifiers.all():
                content[-1][1][-1][2].append(k.modifier_value)
        for j in i.bars.all():
            content[-1][2].append([j.max_value, j.negative_value, lobby.lobby_parameter_bars.all()[j.bar_id].color])

    lobby.update_parameters.all().delete()
    lobby.update_create_items.all().delete()
    lobby.update_item_description.all().delete()
    lobby.update_item_names.all().delete()
    lobby.update_delete_items.all().delete()
    lobby.update_create_item_modifier.all().delete()
    lobby.update_item_modifier.all().delete()
    lobby.update_delete_item_modifier.all().delete()

    context['lobby_name'] = lobby_name
    context['players'] = players
    context['parameters'] = parameters
    context['content'] = content
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