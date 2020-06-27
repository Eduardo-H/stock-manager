from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

# Create your views here.
def home(request):
    dados = AlocacaoRecolhimento.objects.all()
    return render(request, 'management/home.html', {'dados':dados})

def criaralocacao(request):
    itens = Item.objects.all()
    viaturas = Viatura.objects.all()
    agentes = Agente.objects.all()

    if request.method == 'GET':
        return render(request, 'management/criaralocacao.html',
                {'formulario':FormAlocacao(), 'itens':itens, 'viaturas':viaturas, 'agentes':agentes}
            )
    else:
        try:
            formulario = FormAlocacao(request.POST)
            agente1 = request.POST['agente-1']
            agente2 = request.POST['agente-2']

            print(agente1)

            if agente2 is not None:
                print(agente2)
        except ValueError:
            return render(request, 'management/criaralocacao.html',
                    {'formulario':FormAlocacao(), 'itens':itens, 'viaturas':viaturas, 'agentes':agentes, 'erro':'Não foi possível cadastrar a alocação'}
                )

def detalhealocacao(request, pk_alocacao):
    if request.method == 'GET':
        alocacao = get_object_or_404(Alocacao, pk=pk_alocacao)
        return render(request, 'management/detalhealocacao.html', {'alocacao':alocacao})

def menuestoque(request):
    itensestoque = Estoque.objects.all()
    itensperdidoextraviado = ItemPerdidoExtraviado.objects.all()
    return render(request, 'management/menuestoque.html', {'itensestoque':itensestoque, 'itensperdidoextraviado':itensperdidoextraviado})

def adicionarestoque(request):
    itens = Item.objects.all()
    if request.method == 'GET':
        return render(request, 'management/adicionarestoque.html', {'itens':itens})
    else:
        try:
            estoque = get_object_or_404(Estoque, pk=request.POST['item'])
            quantidade = request.POST['quantidade']
            quantidade = int(quantidade)
            estoque.quantidade += quantidade
            estoque.save()
            return redirect('menuestoque')
        except ValueError:
            return render(request, 'management/adicionarestoque.html', {'itens':itens, 'erro':'Não foi possível adicionar ao estoque'})
