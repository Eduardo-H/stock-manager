from django.forms import ModelForm
from .models import *

class FormAlocacao(ModelForm):
    class Meta:
        model = Alocacao
        fields = ['data', 'horario', 'item', 'quantidade', 'turno', 'local', 'motivo']

class FormRecolhimento(ModelForm):
    class Meta:
        model = Recolhimento
        fields = ['data', 'horario', 'alocacao']
