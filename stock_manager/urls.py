"""stock_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from management import views

urlpatterns = [
    path('', views.home, name='home'),
    path('alocacao/', views.menualocacao, name='menualocacao'),
    path('alocacao/criar-alocacao/', views.criaralocacao, name='criaralocacao'),
    path('alocacao/<int:pk_alocacao>/detalhes', views.detalhealocacao, name='detalhealocacao'),
    path('alocacao/procurar-por-tipo/', views.procurarportipo, name='procurarportipo'),
    path('alocacao/alocacoes-em-aberto', views.alocacoesabertas, name='alocacoesabertas'),
    path('recolhimento/', views.menurecolhimento, name='menurecolhimento'),
    path('recolhimento/<int:pk_alocacao>/cadastar/', views.cadastrarrecolhimento, name='cadastrarrecolhimento'),
    path('recolhimento/<int:pk_recolhimento>/detalhes/', views.detalherecolhimento, name='detalherecolhimento'),
    path('agente/', views.menuagente, name='menuagente'),
    path('agente/cadastrar-agente/', views.cadastraragente, name='cadastraragente'),
    path('agente/<int:pk_agente>/detalhes/', views.detalheagente, name='detalheagente'),
    path('agente/<int:pk_agente>/editar/', views.editaragente, name='editaragente'),
    path('agente/procurar-agente/', views.procuraragente, name='procuraragente'),
    path('viatura/', views.menuviatura, name='menuviatura'),
    path('viatura/cadastrar-viatura/', views.cadastrarviatura, name='cadastrarviatura'),
    path('estoque/', views.menuestoque, name='menuestoque'),
    path('estoque/adicionar-ao-estoque/', views.adicionarestoque, name='adicionarestoque'),
    path('estoque/cadastrar-item/', views.cadastraritem, name="cadastraritem"),
    path('estoque/itens-perdidos-extraviados/', views.menuitemperdido, name="menuitemperdido"),

    path('admin/', admin.site.urls),
]
