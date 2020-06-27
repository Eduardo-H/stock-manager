from django.forms import ModelForm
from django import forms
from .models import *

class FormAlocacao(ModelForm):
    class Meta:
        model = Alocacao
        fields = ['data', 'horario', 'item', 'quantidade', 'turno', 'local', 'motivo']

    data = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y')
    )

class FormRecolhimento(ModelForm):
    class Meta:
        model = Recolhimento
        fields = ['data', 'horario', 'alocacao']

    data = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y')
    )
