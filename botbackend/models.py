from django.db import models
from django.urls import reverse

class Chatusers(models.Model):
    chatid = models.TextField(verbose_name='Идентификатор чата')
    name = models.CharField(max_length=110, verbose_name='Имя пользователя', default=None, blank=True, null=True)
    isactive = models.BooleanField(verbose_name='Запись активна', default=False)
    curstep = models.ForeignKey('Pack', verbose_name='Текущая колода', on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            ]
    
    def __str__(self) -> str:
        return f'{self.name} ({self.chatid})'
    
    def get_absolute_url(self): 
        return reverse('chatuser_list')

class Pack(models.Model):
    class Packtypes(models.TextChoices):
        TXT = 'TXT', 'Текстовая колода'
        IMG = 'IMG', 'Колода с рисунками'

    order = models.IntegerField(verbose_name='Номер вывода')
    name = models.CharField(max_length=50, verbose_name='Имя колоды', unique=True)
    packtype = models.CharField(max_length=3, choices=Packtypes.choices, default=Packtypes.TXT, verbose_name='Тип колоды')
    
    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['name']),
            ]
    
    def __str__(self) -> str:
        return f'{self.order} {self.name}'
    
    def get_absolute_url(self): 
        return reverse('pack_list')

class Card(models.Model):
    pack = models.ForeignKey('Pack', verbose_name='Колода', on_delete=models.CASCADE, blank=False)
    number = models.CharField(max_length=3, verbose_name='Отображаемое число')
    cardtext = models.TextField(verbose_name='Текст или ссылка на файл')

    class Meta:
        ordering = ['pack', 'number']

    def __str__(self) -> str:
        return f'{self.number}: {self.cardtext}'

    def get_absolute_url(self): 
        return reverse('card_list_all')

class Steplist(models.Model):
    stepname = models.CharField(max_length=50, verbose_name='Имя шага')
    funcname = models.CharField(max_length=50, verbose_name='Функция теущего шага')

    def __str__(self) -> str:
        return self.stepname

    def get_absolute_url(self): 
        return reverse('steps_list')

#class 
