from django.forms import ModelForm
from django import forms
from .models import *

class FormAlocacao(ModelForm):
    class Meta:
        model = Alocacao
        fields = ['data', 'horario', 'item', 'quantidade', 'turno', 'rua', 'numero', 'bairro', 'complemento', 'motivo']

    data = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
    )


class FormRecolhimento(ModelForm):
    class Meta:
        model = Recolhimento
        fields = ['data', 'horario', 'quantidade', 'turno']

    data = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
    )

class FormItem(ModelForm):
    class Meta:
        model = Item
        fields = ['nome']

class FormAgente(ModelForm):
    class Meta:
        model = Agente
        fields = ['nome', 'sexo', 'gritodeguerra']

class FormViatura(ModelForm):
    class Meta:
        model = Viatura
        fields = ['numero', 'placa']

class FormPerda(ModelForm):
    class Meta:
        model = ItemPerdidoExtraviado
        fields = ['data', 'horario', 'quantidade']

    data = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y', )
    )
