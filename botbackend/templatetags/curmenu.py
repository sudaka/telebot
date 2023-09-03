from django import template
from django.urls import path, include, resolve, reverse

register = template.Library()

class MenuItem():
    def __init__(self, menutext, menulink = '#', newwindow = False, is_staff = False):
        self.menutext = menutext
        self.menulink = menulink
        self.newwindow = newwindow
        self.is_staff = is_staff

@register.inclusion_tag('curmenu_left.html', takes_context=True)
def showleftmenu(context):
    curleftmenu = []
    menu = MenuItem('НАСТРОЙКА БОТА', menulink='#', newwindow=False, is_staff=True)
    curleftmenu.append(menu)
    menu = MenuItem('Список колод', reverse('pack_list'), newwindow=False, is_staff=True)
    curleftmenu.append(menu)
    menu = MenuItem('Список карт', reverse('card_list_all'), newwindow=False, is_staff=True)
    curleftmenu.append(menu)
    menu = MenuItem('Список клиентов бота', reverse('chatuser_list'), newwindow=False, is_staff=True)
    curleftmenu.append(menu)
    menu = MenuItem('АДМИНИСТРИРОВАНИЕ СЕРВЕРА', menulink='#', newwindow=False, is_staff=True)
    curleftmenu.append(menu)
    menu = MenuItem('Функции для шагов', reverse('steps_list'), newwindow=False, is_staff=True)
    curleftmenu.append(menu)
    menu = MenuItem('Системные пользователи', reverse('admin:auth_user_changelist'), newwindow=True, is_staff=True)
    curleftmenu.append(menu)
   
    return {'leftmenu': curleftmenu, 'user': context['user']}