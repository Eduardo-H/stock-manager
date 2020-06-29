from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

# Create your views here.
def home(request):
    dados = AlocacaoRecolhimento.objects.all()
    return render(request, 'management/home.html', {'dados':dados})

# ALOCAÇÃO

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

# AGENTES
def menuagente(request):
    agentes = Agente.objects.all()
    return render(request, 'management/menuagente.html', {'agentes':agentes})

def cadastraragente(request):
    if request.method == 'GET':
        agente = Agente()
        return render(request, 'management/cadastraragente.html', {'formulario':FormAgente(), 'agente':agente})
    else:
        try:
            formulario = FormAgente(request.POST)
            formulario.save()
            return redirect('menuagente')
        except ValueError:
            return render(request, 'management/cadastraragente.html', {'formulario':FormAgente(), 'erro':'Não foi possível cadastrar o agente'})

def detalheagente(request, pk_agente):
    agente = get_object_or_404(Agente, pk=pk_agente)
    alocacoes = AlocacaoAgente.objects.filter(agente_id=agente.id)
    recolhimentos = RecolhimentoAgente.objects.filter(agente_id=agente.id)
    return render(request, 'management/detalheagente.html', {'agente':agente, 'alocacoes':alocacoes, 'recolhimentos':recolhimentos})



# ESTOQUE
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
            estoque = Estoque.objects.get(item_id=request.POST['item'])
            quantidade = request.POST['quantidade']
            quantidade = int(quantidade)
            estoque.quantidade += quantidade
            estoque.save()
            return redirect('menuestoque')
        except ValueError:
            return render(request, 'management/adicionarestoque.html', {'itens':itens, 'erro':'Não foi possível adicionar ao estoque'})

def cadastraritem(request):
    if request.method == 'GET':
        return render(request, 'management/cadastraritem.html', {'formulario':FormItem()})
    else:
        try:
            formulario = FormItem(request.POST)
            item = formulario.save(commit=False)
            estoque = Estoque()
            estoque.item = item
            quantidade = request.POST['quantidade']
            quantidade = int(quantidade)
            estoque.quantidade = quantidade
            item.save()
            estoque.save()
            return redirect('menuestoque')
        except ValueError:
            return render(request, 'management/cadastraritem.html', {'formulario':FormItem(), 'erro':'Não foi possível adicionar o item'})

def editaritem(request, pk_item):
    item = get_object_or_404(Item, pk=pk_item)
    if request.method == 'GET':
        return render(request, 'management/editaritem.html', {'item':item})

def deletaritem(request):
    if request.method == 'POST':
        try:
            item = get_object_or_404(Item, pk=request.POST['item'])
            estoque = Estoque.objects.get(item_id=request.POST['item'])
            print(item)
            print(estoque)
            item.delete()
            estoque.delete()
            return redirect('menuestoque')
        except ValueError:
            return render(request, 'management/menuestoque.html',
                {'itensestoque':itensestoque, 'itensperdidoextraviado':itensperdidoextraviado, 'erro':'Não foi possível excluír o item'}
            )
