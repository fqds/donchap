from django import forms

from master.models import Lobby
class CreateLobbyForm(forms.Form):
    lobby_name = forms.CharField(max_length=16, label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':60,'rows':22}), label='', initial=(
'''Имя
Раса
Класс
Уровень level
Сила S
Выносливость E
Ловкость A
Восприятие P
Интеллект I
Харизма C
Здоровье HP S*4+E*10
Мана MP I*10+P*25+E*15
Резист RES 0
Уворот DODGE A*5+P*5
УронБлижний DMG S*3+A*1
УронДальний RDMG A*1+I*2+P*2
УронМагический MDMG I*7+P*3'''))
