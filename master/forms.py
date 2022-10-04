from django import forms

from master.models import Lobby
class CreateLobbyForm(forms.Form):
    lobby_name = forms.CharField(max_length=16, label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':60,'rows':22}), label='', initial=(
'''name Имя
level Уровень
species Расса
class Класс
strength Сила S
endurance Выносливость E
agility Ловкость A
perception Восприятие P
intellect Интеллект I
charisma Харизма C
health_points Здоровье HP S*4+E*10
mana_points Мана MP I*10+P*25*E*15
resistance Резист RES 0
dodge Уворот DODGE A*5+P*5
dmg_melee УронБлижний DMG S*3+A*1
dmg_ranged УронДальний RDMG A*1+I*2+P*2
dmg_magical УронМагический MDMG I*7+P*3
buffs Баффы
cash Деньги
inventory Инвентарь'''))
