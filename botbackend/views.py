from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from .models import Pack, Card, Steplist, Chatusers
from django.urls import reverse_lazy
import bot
import cupidongame.settings as cursettings
import imgcreator
import os

@login_required
def packlist(request):
    packs = Pack.objects.all()
    return render(request, 'pack_list.html', {'packs': packs})

class PackCreateView(LoginRequiredMixin, CreateView):
    model = Pack
    fields = ['packtype', 'order', 'name']
    template_name = 'pack_create.html'

class PackUpdateView(LoginRequiredMixin, UpdateView):
    model = Pack
    fields = ['packtype', 'order', 'name']
    template_name = 'pack_edit.html'
    success_url = reverse_lazy('pack_list')

class PackDeleteView(LoginRequiredMixin, DeleteView):
    model = Pack
    context_object_name = 'name'
    template_name = 'pack_del.html'
    success_url = reverse_lazy('pack_list')

@login_required
def cardlist(request):
    cards = Card.objects.all()
    return render(request, 'card_list.html', {'cards': cards})

class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    fields = ['pack', 'number', 'cardtext']
    template_name = 'card_create.html'

class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    fields = ['pack', 'number', 'cardtext']
    template_name = 'card_edit.html'
    success_url = reverse_lazy('card_list_all')

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    context_object_name = 'cardtext'
    template_name = 'card_del.html'
    success_url = reverse_lazy('card_list_all')

@login_required
def stepslist(request):
    steps = Steplist.objects.all()
    return render(request, 'steps_list.html', {'steps': steps})

class StepsCreateView(LoginRequiredMixin, CreateView):
    model = Steplist
    fields = ['stepname', 'funcname']
    template_name = 'steps_create.html'

class StepsUpdateView(LoginRequiredMixin, UpdateView):
    model = Steplist
    fields = ['stepname', 'funcname']
    template_name = 'steps_edit.html'
    success_url = reverse_lazy('steps_list')

class StepsDeleteView(LoginRequiredMixin, DeleteView):
    model = Steplist
    context_object_name = 'stepname'
    template_name = 'steps_del.html'
    success_url = reverse_lazy('steps_list')

@login_required
def chatuserlist(request):
    chatusers = Chatusers.objects.all()
    return render(request, 'chatuser_list.html', {'chatusers': chatusers})

@login_required
def chatuseractivate(request, pk):
    activateduser = get_object_or_404(Chatusers, pk = pk)
    activateduser.isactive = True
    activateduser.save()
    bot.sendactivatemessage(activateduser.chatid)
    return redirect('chatuser_list')

@login_required
def chatuserdeactivate(request, pk):
    activateduser = get_object_or_404(Chatusers, pk = pk)
    activateduser.isactive = False
    activateduser.save()
    return redirect('chatuser_list')

@login_required
def pagenerator(request):
    pagenparams = {}
    pagenparams['Директория хранения изображений'] = cursettings.PAGEN_BACKGROUND_ROOT
    pagenparams['Файл фона изображений'] = cursettings.PAGEN_BACKGROUND_FILE
    pagenparams['Процент заполнения текстом'] = cursettings.PAGEN_SQUAREFORTEXT
    pagenparams['Файл шрифта'] = cursettings.PAGEN_FONTFILE
    return render(request, 'messages.html', {"pagenparams" : pagenparams})

@login_required
def generateimg(request):
    imgdir = cursettings.PAGEN_BACKGROUND_ROOT
    backimg = cursettings.PAGEN_BACKGROUND_FILE
    textpercent = cursettings.PAGEN_SQUAREFORTEXT
    fontfile = cursettings.PAGEN_FONTFILE
    packs = Pack.objects.filter(packtype__exact=Pack.Packtypes.CTJ)
    for curpack in packs:
        cards = Card.objects.filter(pack__exact=curpack)
        for card in cards:
            m = imgcreator.Multiline(card.cardtext)
            genfname = m.createfilename(backimg, fontfile, textpercent)
            fullpath = os.path.join(imgdir, f'{genfname}_{backimg}')
            if m.checkfilebyname(fullpath):
                continue
            else:
                try:
                    m.createjpgmessage(backimg, fontfile, textpercent, imgdir)
                except Exception as e:
                    pass
    return render(request, 'messagefinish.html')