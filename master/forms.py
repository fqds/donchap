from django import forms

from master.models import Lobby
class CreateLobbyForm(forms.Form):
    lobby_name = forms.CharField(max_length=16, label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':60,'rows':22}), label='', initial=(
'''Имя
Раса
Класс
Уровень LEVEL
Сила СИЛ
Выносливость ВЫН
Ловкость ЛВК
Восприятие ВОС
Интеллект ИНТ
Харизма ХАРИЗМА
ПотерянноеЗдоровье LOSTHP
ПотеряннаяМана LOSTMP
Резист РЕЗИСТ 0
Уворот УВОРОТ ЛВК*5+ВОС*5
УронБлижний БЛИЖ_УРОН (СИЛ*3+ЛВК)*LEVEL
УронДальний ДАЛЬН_УРОН (ЛВК+ИНТ*2+ВОС*2)*LEVEL
УронМагический МАГ_УРОН (ИНТ*7+ВОС*3)*LEVEL
Здоровье ЗДОРОВЬЕ (СИЛ*4+ВЫН*10)*LEVEL LOSTHP red
Мана МАНА ИНТ*10+ВОС*25+ВЫН*15 LOSTMP blue'''))
