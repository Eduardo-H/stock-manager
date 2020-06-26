from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

# Create your views here.
def home(request):
    dados = AlocacaoRecolhimento.objects.all()
    return render(request, 'management/home.html', {'dados':dados})

def criaralocacao(request):
    if requet.method == 'GET':
        return render(request, 'management/criaralocacao.html', {'formulario':FormAlocacao()})



def detalhealocacao(request, pk_alocacao):
    if request.method == 'GET':
        alocacao = get_object_or_404(Alocacao, pk=pk_alocacao)
        return render(request, 'management/detalhealocacao.html', {'alocacao':alocacao})
