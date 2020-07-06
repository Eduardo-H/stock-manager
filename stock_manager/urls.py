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
    path('alocacao/', views.menu_alocacao, name='menu_alocacao'),
    path('alocacao/criar-alocacao/', views.criar_alocacao, name='criar_alocacao'),
    path('alocacao/<int:pk_alocacao>/detalhes', views.detalhe_alocacao, name='detalhe_alocacao'),
    path('alocacao/procurar-por-tipo/', views.procurar_por_tipo_alocacao, name='procurar_por_tipo_alocacao'),
    path('alocacao/alocacoes-em-aberto', views.alocacoes_abertas, name='alocacoes_abertas'),
    path('recolhimento/', views.menu_recolhimento, name='menu_recolhimento'),
    path('recolhimento/<int:pk_alocacao>/cadastar/', views.cadastrar_recolhimento, name='cadastrar_recolhimento'),
    path('recolhimento/<int:pk_recolhimento>/detalhes/', views.detalhe_recolhimento, name='detalhe_recolhimento'),
    path('recolhimento/procurar-por-tipo/', views.procurar_por_tipo_recolhimento, name='procurar_por_tipo_recolhimento'),
    path('agente/', views.menu_agente, name='menu_agente'),
    path('agente/cadastrar-agente/', views.cadastrar_agente, name='cadastrar_agente'),
    path('agente/<int:pk_agente>/detalhes/', views.detalhe_agente, name='detalhe_agente'),
    path('agente/<int:pk_agente>/editar/', views.editar_agente, name='editar_agente'),
    path('agente/procurar-agente/', views.procurar_agente, name='procurar_agente'),
    path('viatura/', views.menu_viatura, name='menu_viatura'),
    path('viatura/cadastrar-viatura/', views.cadastrar_viatura, name='cadastrar_viatura'),
    path('estoque/', views.menu_estoque, name='menu_estoque'),
    path('estoque/adicionar-ao-estoque/', views.adicionar_estoque, name='adicionar_estoque'),
    path('estoque/cadastrar-item/', views.cadastrar_item, name='cadastrar_item'),
    path('estoque/itens-perdidos-extraviados/', views.menu_item_perdido, name='menu_item_perdido'),
    path('estoque/itens-perdidos-extraviados/<int:pk_perda_extravio>/detalhes', views.detalhe_item_perdido, name='detalhe_item_perdido'),

    path('admin/', admin.site.urls),
]
