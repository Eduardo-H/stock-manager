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
    if request.method == 'GET':
        return render(request, 'management/detalheagente.html', {'agente':agente, 'alocacoes':alocacoes, 'recolhimentos':recolhimentos})
    else:
        try:
            agente = get_object_or_404(Agente, pk=request.POST['agente'])
            agente.delete()
            return redirect('menuagente')
        except:
            return render(request, 'management/detalheagente.html',
                {'agente':agente, 'alocacoes':alocacoes, 'recolhimentos':recolhimentos, 'erro':'Não foi possível deletar este agente'}
            )

def editaragente(request, pk_agente):
    agente = get_object_or_404(Agente, pk=pk_agente)
    if request.method == 'GET':
        formulario = FormAgente(instance=agente)
        return render(request, 'management/editaragente.html', {'agente':agente, 'formulario':formulario})
    else:
        try:
            formulario = FormAgente(request.POST, instance=agente)
            formulario.save()
            return redirect('menuagente')
        except ValueError:
            return render(request, 'management/editaragente.html',
                {'agente':agente, 'formulario':formulario, 'erro':'Não foi possível editar o agente'}
            )

# VIATURAS
def menuviatura(request):
    viaturas = Viatura.objects.all()
    if request.method == 'GET':
        return render(request, 'management/menuviatura.html', {'viaturas':viaturas})
    else:
        if 'viatura' in request.POST:
            try:
                viatura = get_object_or_404(Viatura, pk=request.POST['viatura'])
                viatura.delete()
                return render(request, 'management/menuviatura.html', {'viaturas':viaturas, 'confirmacao':'Viatura deletado com sucesso'})
            except ValueError:
                return render(request, 'management/menuviatura.html', {'viaturas':viaturas, 'erro':'Não foi possível deletar a viatura'})
        elif 'numero' in request.POST:
            try:
                viatura = Viatura.objects.get(numero=request.POST['numeroAntigo'])
                viatura.numero = request.POST['numero']
                viatura.placa = request.POST['placa']
                viatura.save()
                return render(request, 'management/menuviatura.html', {'viaturas':viaturas, 'confirmacao':'Viatura editada com sucesso'})
            except ValueError:
                return render(request, 'management/menuviatura.html', {'viaturas':viaturas, 'erro':'Não foi possível editar a viatura'})

def cadastrarviatura(request):
    if request.method == 'GET':
        return render(request, 'management/cadastrarviatura.html', {'formulario':FormViatura()})
    else:
        numero = request.POST['numero']
        placa = request.POST['placa']
        print(numero)
        numero = Viatura.objects.filter(numero=numero)
        print(numero)
        if not numero:
            if len(placa) == 7:
                placa = Viatura.objects.filter(placa=placa)
                print(placa)
                if not placa:
                    try:
                        formulario = FormViatura(request.POST)
                        formulario.save()
                        return redirect('menuviatura')
                    except ValueError:
                        return render(request, 'management/cadastrarviatura.html', {'formulario':FormViatura(), 'erro':'Não foi possível cadastrar a viatura'})
                else:
                    return render(request, 'management/cadastrarviatura.html', {'formulario':FormViatura(), 'erroPlaca':'Essa placa já foi cadastrada'})
            else:
                return render(request, 'management/cadastrarviatura.html', {'formulario':FormViatura(), 'erroPlaca':'A placa deve ter 7 caracteres, sem simbolos'})
        else:
            return render(request, 'management/cadastrarviatura.html', {'formulario':FormViatura(), 'erroNumero':'Viatura existente com este número'})


# ESTOQUE
def menuestoque(request):
    itensestoque = Estoque.objects.all()
    itensperdidoextraviado = ItemPerdidoExtraviado.objects.all()
    if request.method == 'GET':
        return render(request, 'management/menuestoque.html', {'itensestoque':itensestoque, 'itensperdidoextraviado':itensperdidoextraviado})
    else:
        if 'item' in request.POST: # Verifica se o botão de 'submit' foi do formulário de deleção
            try:
                item = get_object_or_404(Item, pk=request.POST['item'])
                itemestoque = Estoque.objects.get(item_id=item.id)
                itemestoque.delete()
                item.delete()
                return render(request, 'management/menuestoque.html',
                    {'itensestoque':itensestoque, 'itensperdidoextraviado':itensperdidoextraviado, 'confirmacao':'Item excluído com sucesso!'}
                )
            except ValueError:
                return render(request, 'management/menuestoque.html',
                    {'itensestoque':itensestoque, 'itensperdidoextraviado':itensperdidoextraviado, 'erro':'Não foi possível excluir o item'}
                )
        elif 'nomeNovo' in request.POST: # Verifica se o botão de 'submit' foi do formulário de edição
            try:
                item = Item.objects.get(nome=request.POST['nomeAntigo'])
                item.nome = request.POST['nomeNovo']
                item.save()
                return render(request, 'management/menuestoque.html',
                    {'itensestoque':itensestoque, 'itensperdidoextraviado':itensperdidoextraviado, 'confirmacao':'Item editado com sucesso!'}
                )
            except ValueError:
                return render(request, 'management/menuestoque.html',
                    {'itensestoque':itensestoque, 'itensperdidoextraviado':itensperdidoextraviado, 'erro':'Não foi possível editar o item'}
                )

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
