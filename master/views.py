from django.shortcuts import render, redirect

from master.forms import CreateLobbyForm
from master.models import Lobby, LobbyParameter

def create_lobby_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return redirect('entrance')
    

    if request.POST:
        form = CreateLobbyForm(request.POST)
        print(form)
        lobby_name = form.cleaned_data.get('lobby_name')
        raw_content = form.cleaned_data.get('content')
        lobby = Lobby(lobby_name=lobby_name)
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
        #render(request, redirect("lobby/" + lobby_name))
    else:
        form = CreateLobbyForm()
    context = {'form': form}
    return render(request, "master/create_lobby.html", context)