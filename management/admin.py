from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Alocacao)
admin.site.register(Recolhimento)
admin.site.register(AlocacaoRecolhimento)
admin.site.register(AlocacaoAgente)
admin.site.register(RecolhimentoAgente)
admin.site.register(Agente)
admin.site.register(Viatura)
admin.site.register(Item)
admin.site.register(Estoque)
admin.site.register(ItemPerdidoExtraviado)
