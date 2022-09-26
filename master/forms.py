from django import forms

from master.models import Lobby
class CreateLobbyForm(forms.Form):
    lobby_name = forms.CharField(max_length=16, label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':60,'rows':22}), label='', initial=('''a Имя
a Уровень
a Расса
a Класс
b Сила S
b Выносливость E
b Ловкость A
b Восприятие P
b Интеллект I
b Харизма C
c Здоровье HP S*4+E*10
c Мана MANA I*10+P*25*E*15
c Резист RES 0
c Уворот DODGE A*5+P*5
c УронБлижний DMG S*3+A*1
c УронДальний RDMG A*1+I*2+P*2
c УронМагический MDMG I*7+P*3
d Баффы
d Деньги
d Инвентарь'''))
