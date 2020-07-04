from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import *
from .forms import *
import datetime

def home(request):
    alocacoesrecolhimentos = AlocacaoRecolhimento.objects.all().order_by('-id')[:50]
    return render(request, 'management/home.html', {'alocacoesrecolhimentos':alocacoesrecolhimentos})

#############
# ALOCAÇÕES #
#############
def menualocacao(request):
    alocacoes = Alocacao.objects.all().order_by('-id')
    return render(request, 'management/menualocacao.html', {'alocacoes':alocacoes})

def criaralocacao(request):
    itens = Item.objects.all()
    viaturas = Viatura.objects.all().order_by('numero')
    agentes = Agente.objects.all().order_by('nome')

    if request.method == 'GET':
        return render(request, 'management/criaralocacao.html',
                {'formulario':FormAlocacao(), 'itens':itens, 'viaturas':viaturas, 'agentes':agentes}
            )
    else:
        agente1 = request.POST['agente-1'] # Recebe o ID do primeiro agente, e do segundo, se houver
        agente2 = request.POST['agente-2']
        agente1 = get_object_or_404(Agente, pk=agente1) # Recebe o objeto 'Agente 1'

        quantidade = request.POST['quantidade'] # Recebe a quantidade do item informada
        estoque = Estoque.objects.get(item=request.POST['item']) # Recebe o item no estoque escolhido
        disponibilidade = estoque.quantidade - int(quantidade) # Calcula a quantidade disponível no estoque com a informada

        if disponibilidade >= 0: # Verifica se a quantidade é valida
            if 'viaturaId' in request.POST: # Verifica se o método de seleção de viatura é do tipo SELECT
                if request.POST['viaturaId'] != '-': # Verifica se o usuário selecionou uma opção diferente da padrão ('-')
                    viatura = get_object_or_404(Viatura, pk=request.POST['viaturaId']) # Recebe o objeto 'Viatura'
                    if viatura is not None: # Verifica se foi retornado um objeto
                        try:
                            formulario = FormAlocacao(request.POST)
                            salvaralocacao(formulario, viatura, agente1, agente2, request.POST['cadastrador']) # Função para a persistência de dados

                            return redirect('menualocacao')
                        except ValueError:
                            return render(request, 'management/criaralocacao.html',
                                    {'formulario':FormAlocacao(), 'itens':itens, 'viaturas':viaturas, 'agentes':agentes, 'erro':'Não foi possível cadastrar a alocação'}
                                )
                elif request.POST['viaturaId'] == '-': # Se o usuário não selecionou uma opção difente da padrão
                    try:
                        formulario = FormAlocacao(request.POST)
                        viatura = None # Atribui o valor None para que na função abaixo não seja feita a persistência da viatura na alocação
                        salvaralocacao(formulario, viatura, agente1, agente2, request.POST['cadastrador'])

                        return redirect('menualocacao')
                    except ValueError:
                        return render(request, 'management/criaralocacao.html',
                                {'formulario':FormAlocacao(), 'itens':itens, 'viaturas':viaturas, 'agentes':agentes, 'erro':'Não foi possível cadastrar a alocação'}
                            )
            elif 'viaturaNumero' in request.POST: # Verifica se o método de seleção de viatura é do tipo INPUT
                viatura = Viatura.objects.get(numero=request.POST['viaturaNumero']) # Recebe o objeto 'Viatura' de acordo com o número provido
                if viatura is not None: # Verifica se foi retornado um objeto
                    try:
                        formulario = FormAlocacao(request.POST)
                        salvaralocacao(formulario, viatura, agente1, agente2, request.POST['cadastrador'])

                        return redirect('menualocacao')
                    except ValueError:
                        return render(request, 'management/criaralocacao.html',
                                {'formulario':FormAlocacao(), 'itens':itens, 'viaturas':viaturas, 'agentes':agentes, 'erroViatura':'Viatura inexistente'}
                            )
                else:
                    try:
                        formulario = FormAlocacao(request.POST)
                        viatura = None
                        salvaralocacao(formulario, viatura, agente1, agente2, request.POST['cadastrador'])

                        return redirect('menualocacao')
                    except ValueError:
                        return render(request, 'management/criaralocacao.html',
                                {'formulario':FormAlocacao(), 'itens':itens, 'viaturas':viaturas, 'agentes':agentes, 'erro':'Não foi possível cadastrar a alocação'}
                            )
        else:
            return render(request, 'management/criaralocacao.html',
                    {'formulario':FormAlocacao(), 'itens':itens, 'viaturas':viaturas, 'agentes':agentes, 'erroQuantidade':'Número superior ao estoque'}
                )
"""
FUNÇÃO PARA A PERSISTÊNCIA DE UMA ALOCAÇÃO NO BANCO DE DADOS
"""
def salvaralocacao(formulario, viatura, agente1, agente2, cadastrador):
    alocacao = formulario.save(commit=False)
    if viatura is not None:
        alocacao.viatura = viatura

    alocacao.cadastrador = get_object_or_404(User, pk=cadastrador)
    alocacao.status = 'Aberto'
    alocacao.save()

    estoque = Estoque.objects.get(item=alocacao.item)
    estoque.quantidade -= int(alocacao.quantidade)
    estoque.save()

    alocacaoRecolhimento = AlocacaoRecolhimento()
    alocacaoRecolhimento.alocacao = alocacao
    alocacaoRecolhimento.save()

    alocacaoAgente = alocacao.id
    alocacaoAgente = get_object_or_404(Alocacao, pk=alocacaoAgente)

    agenteAlocacao1 = AlocacaoAgente()
    agenteAlocacao1.alocacao = alocacaoAgente
    agenteAlocacao1.agente = agente1
    agenteAlocacao1.save()

    if agente2 != '-':
        agente2 = get_object_or_404(Agente, pk=agente2)
        agenteAlocacao2 = AlocacaoAgente()
        agenteAlocacao2.alocacao = alocacaoAgente
        agenteAlocacao2.agente = agente2
        agenteAlocacao2.save()

def detalhealocacao(request, pk_alocacao):
    alocacao = get_object_or_404(Alocacao, pk=pk_alocacao)
    agentes = AlocacaoAgente.objects.filter(alocacao_id=pk_alocacao)
    if request.method == 'GET':
        return render(request, 'management/detalhealocacao.html', {'alocacao':alocacao, 'agentes':agentes})
    else:
        try:
            if 'alocacaoDesativar' in request.POST:
                alocacao = get_object_or_404(Alocacao, pk=request.POST['alocacaoDesativar'])
                alocacao.status = 'Desativado'
                alocacao.save()
                return render(request, 'management/detalhealocacao.html', {'alocacao':alocacao, 'agentes':agentes, 'confirmacao':'Alocação desativada com sucesso!'})
            elif 'alocacaoAtivar' in request.POST:
                alocacao = get_object_or_404(Alocacao, pk=request.POST['alocacaoAtivar'])
                alocacao.status = 'Aberto'
                alocacao.save()
                return render(request, 'management/detalhealocacao.html', {'alocacao':alocacao, 'agentes':agentes, 'confirmacao':'Alocação reativada com sucesso!'})

        except ValueError:
            return render(request, 'management/detalhealocacao.html', {'alocacao':alocacao, 'agentes':agentes, 'erro':'Não foi possível desativar a alocação'})

def alocacoesabertas(request):
    lista_alocacoes = Alocacao.objects.filter(status='Aberto')
    paginator = Paginator(lista_alocacoes, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        alocacoes = paginator.page(page)
    except(EmptyPage, InvalidPage):
        alocacoes = paginator.page(paginator.num_pages)

    return render(request, 'management/alocacoesabertas.html', {'alocacoes':alocacoes})

def procurarportipo(request):
    if 'pesquisa' in request.GET:
        tipo = request.GET.get('pesquisa')
        valor = request.GET.get('valor')

        if tipo == 'data': # Verifica se a opção de busca foi 'Data'
            # Mudando o formato da data de 'DD/MM/AAAA' para 'DD/MM/AA'
            if len(valor) == 10:
                data_valida = valor[:8]
                dia, mes, ano = data_valida.split('/')
                valido = True
                try:
                    datetime.datetime(int(ano),int(mes),int(dia))
                except ValueError:
                    valido = False
            else:
                return render(request, 'management/procurarportipo.html', {'resultado':'nenhum'})

            data = mudarformato(valor)

            if len(data) == 10 and data[4] == '-' and data[7] == '-':
                # O IF abaixo basicamente verifica se a data informada é inválida
                if not valido:
                    return render(request, 'management/procurarportipo.html', {'resultado':'nenhum'})
                else:
                    alocacoes = Alocacao.objects.filter(data=data).order_by('-data')
                    if alocacoes:
                        alocacoes = paginador(alocacoes)
                        return render(request, 'management/procurarportipo.html', {'alocacoes':alocacoes, 'resultado':'data'})
                    else:
                        return render(request, 'management/procurarportipo.html', {'resultado':'nenhum'})
            else:
                return render(request, 'management/procurarportipo.html', {'resultado':'nenhum'})
        elif tipo == 'item': # Verifica se a opção de busca foi 'Item'
            item = Item.objects.filter(nome=valor)
            if item: # Verifica se exite itens com o nome informado
                item = Item.objects.get(nome=valor)
                alocacoes = Alocacao.objects.filter(item_id=item.id).order_by('-id')
                alocacoes = paginador(alocacoes)
                return render(request, 'management/procurarportipo.html', {'alocacoes':alocacoes, 'resultado':'item'})
            else:
                return render(request, 'management/procurarportipo.html', {'resultado':'nenhum'})
        elif tipo == 'agente': # Verifica se a opção de busca foi 'Agente'
            agente = Agente.objects.filter(gritodeguerra=valor)
            if agente:
                agente = Agente.objects.get(gritodeguerra=valor)
                alocacoes = AlocacaoAgente.objects.filter(agente_id=agente.id).order_by('-id')
                alocacoes = paginador(alocacoes)
                return render(request, 'management/procurarportipo.html', {'alocacoes':alocacoes, 'resultado':'agente'})
            else:
                return render(request, 'management/procurarportipo.html', {'resultado':'nenhum'})
        elif tipo == 'viatura': # Verifica se a opção de busca foi 'Viatura'
            if valor.isdigit():
                viatura = Viatura.objects.filter(numero=valor)
                if viatura:
                    viatura = Viatura.objects.get(numero=valor)
                    alocacoes = Alocacao.objects.filter(viatura_id=viatura.id).order_by('-id')
                    alocacoes = paginador(alocacoes)
                    return render(request, 'management/procurarportipo.html', {'alocacoes':alocacoes, 'resultado':'viatura'})
                else:
                    return render(request, 'management/procurarportipo.html', {'resultado':'nenhum'})
            else:
                return render(request, 'management/procurarportipo.html', {'resultado':'nenhum'})
    else:
        return render(request, 'management/procurarportipo.html', {'dica':'Selecione o tipo desejado e coloque o valor que procura'})


"""
FUNÇÃO PARA A PÁGINAÇÃO
"""
def paginador(lista_resultados):
    paginator = Paginator(lista_resultados, 6) # Retorna 6 resultados para cada página
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        resultado = paginator.page(page)
    except(EmptyPage, InvalidPage):
        resultado = paginator.page(paginator.num_pages)

    return resultado

"""
FUNÇÃO PARA MUDAR O FORMATO DA DATA
"""
def mudarformato(valor):
    # Mudando o formato da data de 'DD/MM/AAAA' para 'AAAA-MM-DD'
    data = valor[6:] + '-'
    data += valor[3:5] + '-'
    data += valor[:2]

    return data


#################
# RECOLHIMENTOS #
#################

def menurecolhimento(request):
    recolhimentos = Recolhimento.objects.all().order_by('-id')
    return render(request, 'management/menurecolhimento.html', {'recolhimentos':recolhimentos})

def cadastrarrecolhimento(request, pk_alocacao):
    alocacao = get_object_or_404(Alocacao, pk=pk_alocacao)
    agentealocacao = AlocacaoAgente.objects.filter(alocacao_id=pk_alocacao) # Busca o(s) agente(s) relacionado(s) à alocação
    agentes = Agente.objects.all().order_by('nome') # Busca os agentes cadastrados no sistema
    viaturas = Viatura.objects.all().order_by('numero')
    quantidadeperdida = ItemPerdidoExtraviado.objects.filter(alocacao_id=alocacao.id) # Buscando os cadastros de perda/extravio com o ID da alocação

    if request.method == 'GET':
        if quantidadeperdida: # Se tiver algum resultado de itens perdidos/extraviados
            numero = int(0)
            for cadastro in quantidadeperdida:
                numero += cadastro.quantidade

            nova_quantidade = alocacao.quantidade - numero
            return render(request, 'management/cadastrarrecolhimento.html',
                    {'formulario':FormRecolhimento(), 'alocacao':alocacao, 'agentes':agentes, 'agentealocacao':agentealocacao, 'viaturas':viaturas, 'quantidadeperdida':nova_quantidade}
                )
        else:
            return render(request, 'management/cadastrarrecolhimento.html',
                    {'formulario':FormRecolhimento(), 'alocacao':alocacao, 'agentes':agentes, 'agentealocacao':agentealocacao, 'viaturas':viaturas}
                )
    else:
        # Se o formulário enviado foi o de itens perdidos/extraviados
        if 'quantidade-perdida' in request.POST:
            quantidade = request.POST['quantidade-perdida'] # Recebe a quantidade do item perdido/extraviado

            if quantidadeperdida is not None: # Verifica se existe cadatro de perda/extravio na atual alocação
                nova_quantidade = alocacao.quantidade
                for cadastro in quantidadeperdida: # Vai lendo a quantidade cadastrada e vai subtraindo com o total
                    nova_quantidade -= cadastro.quantidade

            nova_quantidade -= int(quantidade) # Subtrai a quantitade disponível para cadastrar

            data = mudarformato(request.POST['data-perda'])

            perda = ItemPerdidoExtraviado() # Criando e salvando o cadastro da perda/extravio
            perda.data = data
            perda.horario = request.POST['horario-perda']
            perda.alocacao = alocacao
            perda.quantidade = int(quantidade)
            perda.save()

            return render(request, 'management/cadastrarrecolhimento.html',
                    {'formulario':FormRecolhimento(), 'alocacao':alocacao, 'agentes':agentes, 'agentealocacao':agentealocacao, 'viaturas':viaturas, 'novaquantidade':nova_quantidade}
                )
        # Se o formulário enviado foi o de cadastração de recolhimento
        else:
            agente1 = request.POST['agente-1'] # Recebe o ID do primeiro agente, e do segundo, se houver
            agente2 = request.POST['agente-2']
            agente1 = get_object_or_404(Agente, pk=agente1) # Recebe o objeto 'Agente 1'
            quantidade = request.POST['quantidade'] # Recebe a quantidade do item informada

            perdas = ItemPerdidoExtraviado.objects.filter(alocacao_id=alocacao.id)

            # Verifica se existe cadatro de perda/extravio na atual alocação, se exisitir diminui o valor aceitavel para cadastro do recolhimento
            if perdas:
                total = int(0)
                for perda in perdas:
                    total -= int(perda.quantidade)
                if int(quantidade) < total:
                    return render(request, 'management/cadastrarrecolhimento.html',
                            {'formulario':FormRecolhimento(), 'alocacao':alocacao, 'agentes':agentes, \
                                'agentealocacao':agentealocacao, 'viaturas':viaturas, 'erroNumero':'Valor incorreto, se necessário, cadastre uma perda/extravio'
                            }
                        )
            # Se não houver, verifica se a quantidade digitada é igual a disponível para cadastrar
            else:
                if int(quantidade) < alocacao.quantidade:
                    return render(request, 'management/cadastrarrecolhimento.html',
                            {'formulario':FormRecolhimento(), 'alocacao':alocacao, 'agentes':agentes, \
                                'agentealocacao':agentealocacao, 'viaturas':viaturas, 'erroNumero':'Valor incorreto, se necessário, cadastre uma perda/extravio'
                            }
                        )

            if 'viaturaId' in request.POST:
                if request.POST['viaturaId'] != '-':
                    viatura = get_object_or_404(Viatura, pk=request.POST['viaturaId'])
                    if viatura is not None: # Verifica se foi retornado um objeto
                        try:
                            formulario = FormRecolhimento(request.POST)
                            salvarrecolhimento(formulario, alocacao, viatura, agente1, agente2, request.POST['cadastrador']) # Função para a persistência de dados

                            return redirect('menurecolhimento')
                        except ValueError:
                            return render(request, 'management/cadastrarrecolhimento.html',
                                    {'formulario':FormRecolhimento(), 'alocacao':alocacao, 'agentes':agentes, \
                                        'agentealocacao':agentealocacao, 'viaturas':viaturas, 'erro':'Não foi possível cadastrar o recolhimento'
                                    }
                                )
                elif request.POST['viaturaId'] == '-':
                    try:
                        formulario = FormRecolhimento(request.POST)
                        viatura = None # Atribui o valor None para que na função abaixo não seja feita a persistência da viatura na alocação
                        salvarrecolhimento(formulario, alocacao, viatura, agente1, agente2, request.POST['cadastrador'])

                        return redirect('menurecolhimento')
                    except ValueError:
                        return render(request, 'management/cadastrarrecolhimento.html',
                                {'formulario':FormRecolhimento(), 'alocacao':alocacao, 'agentes':agentes, \
                                    'agentealocacao':agentealocacao, 'viaturas':viaturas, 'erro':'Não foi possível cadastrar o recolhimento'
                                }
                            )
            elif 'viaturaNumero' in request.POST:
                viatura = Viatura.objects.get(numero=request.POST['viaturaNumero']) # Recebe o objeto 'Viatura' de acordo com o número provido
                if viatura is not None: # Verifica se foi retornado um objeto
                    try:
                        formulario = FormRecolhimento(request.POST)
                        salvarrecolhimento(formulario, alocacao, viatura, agente1, agente2, request.POST['cadastrador'])

                        return redirect('menurecolhimento')
                    except ValueError:
                        return render(request, 'management/cadastrarrecolhimento.html',
                                {'formulario':FormRecolhimento(), 'alocacao':alocacao, 'agentes':agentes, \
                                    'agentealocacao':agentealocacao, 'viaturas':viaturas, 'erroViatura':'Viatura inexistente'
                                }
                            )
                else:
                    try:
                        formulario = FormRecolhimento(request.POST)
                        viatura = None
                        salvarrecolhimento(formulario, alocacao, viatura, agente1, agente2, request.POST['cadastrador'])

                        return redirect('menurecolhimento')
                    except ValueError:
                        return render(request, 'management/cadastrarrecolhimento.html',
                                {'formulario':FormRecolhimento(), 'alocacao':alocacao, 'agentes':agentes, \
                                    'agentealocacao':agentealocacao, 'viaturas':viaturas, 'erro':'Não foi possível cadastrar o recolhimento'
                                }
                            )

"""
FUNÇÃO PARA A PERSISTÊNCIA DE UM RECOLHIMENTO NO BANCO DE DADOS
"""
def salvarrecolhimento(formulario, alocacao, viatura, agente1, agente2, cadastrador):
    recolhimento = formulario.save(commit=False)
    if viatura is not None:
        recolhimento.viatura = viatura
    recolhimento.alocacao = alocacao
    recolhimento.cadastrador = get_object_or_404(User, pk=cadastrador)
    recolhimento.save()

    alocacao = Alocacao.objects.get(id=alocacao.id)
    alocacao.status = 'Fechado'
    alocacao.save()

    estoque = Estoque.objects.get(item=alocacao.item)
    estoque.quantidade += int(recolhimento.quantidade)
    estoque.save()

    alocacaoRecolhimento = AlocacaoRecolhimento()
    alocacaoRecolhimento.recolhimento = recolhimento
    alocacaoRecolhimento.save()

    recolhimentoAgente = recolhimento.id
    recolhimentoAgente = get_object_or_404(Recolhimento, pk=recolhimentoAgente)

    agenteRecolhimento1 = RecolhimentoAgente()
    agenteRecolhimento1.recolhimento = recolhimentoAgente
    agenteRecolhimento1.agente = agente1
    agenteRecolhimento1.save()

    if agente2 != '-':
        agente2 = get_object_or_404(Agente, pk=agente2)
        agenteRecolhimento2 = RecolhimentoAgente()
        agenteRecolhimento2.recolhimento = recolhimentoAgente
        agenteRecolhimento2.agente = agente2
        agenteRecolhimento2.save()

def detalherecolhimento(request, pk_recolhimento):
    recolhimento = get_object_or_404(Recolhimento, pk=pk_recolhimento)
    agenterecolhimento = RecolhimentoAgente.objects.filter(recolhimento_id=recolhimento.id)
    agentealocacao = AlocacaoAgente.objects.filter(alocacao_id=recolhimento.alocacao_id)
    perdas = ItemPerdidoExtraviado.objects.filter(alocacao_id=recolhimento.alocacao_id)

    if perdas is not None:
        total = int(0)
        for perda in perdas:
            total += perda.quantidade
        return render(request, 'management/detalherecolhimento.html',
                {'recolhimento':recolhimento, 'agenterecolhimento':agenterecolhimento, 'agentealocacao':agentealocacao, 'perdas':total}
            )
    else:
        return render(request, 'management/detalherecolhimento.html',
                {'recolhimento':recolhimento, 'agenterecolhimento':agenterecolhimento, 'agentealocacao':agentealocacao}
            )


###########
# AGENTES #
###########
def menuagente(request):
    if 'procura_agente' in request.GET:
        agentes = Agente.objects.filter(gritodeguerra__contains=request.GET.get('procura_agente'))
        print(agentes)
        if agentes is not None:
            print('Entrouuuuuuuuuuu')
            agentes = paginador(agentes)
            return render(request, 'management/procuraragente.html', {'agentes':agentes})
        else:
            return render(request, 'management/procuraragente.html')
    else:
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




############
# VIATURAS #
############
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
        numero = Viatura.objects.filter(numero=numero)
        if not numero:
            if len(placa) == 7:
                placa = Viatura.objects.filter(placa=placa)
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

###########
# ESTOQUE #
###########
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

                estoque = Estoque.objects.get(item_id=item.id)
                estoque.quantidade = int(request.POST['quantidade'])
                estoque.save()

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
