from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from .models import Pack, Card, Steplist, Chatusers
from django.urls import reverse_lazy
import bot

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