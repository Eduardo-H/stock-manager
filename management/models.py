from django.db import models
from django.contrib.auth.models import User

class Alocacao(models.Model):
    TURNO_CHOICES = (
        ('Manhã', 'Manhã'),
        ('Tarde', 'Tarde'),
        ('Noite', 'Noite'),
        ('Madrugada', 'Madrugada')
    )

    data = models.DateField()
    horario = models.TimeField()
    item = models.ForeignKey(Item)
    quantidade = models.IntegerField()
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES)
    viatura = models.ForeignKey(Viatura, blank=True)
    local = models.CharField(max_length=250)
    motivo = models.CharField(max_length=100, blank=True)
    cadastrador = models.ForeignKey(User)

    def __str__(self):
        return 'Alocação feita no dia' + self.data + ' em ' + self.local

class AlocacaoAgente(models.Model):
    alocacao = models.ForeignKey(Alocacao)
    agente = models.ForeignKey(Agente)

class Recolhimento(models.Model):
    data = models.DateField()
    horario = models.TimeField()
    alocacao = models.ForeignKey(Alocacao)
    cadastrador = models.ForeignKey(User)

class RecolhimentoAgente(models.Models):
    recolhimento = models.ForeignKey(Recolhimento)
    agente = models.ForeignKey(Agente)

class AlocacaoRecolhimento(models.Model):
    data = models.DateField()
    horario = models.TimeField()
    alocacao = models.ForeignKey(Alocacao, blank=True)
    recolhimento = models.ForeignKey(Recolhimento, blank=True)

class Item(models.Model):
    nome = models.CharField(max_length=100)

class Estoque(models.Model):
    item = models.ForeignKey(Item)
    quantidade = models.IntegerField()

class ItemPerdidoExtraviado(models.Model):
    data = models.DateField()
    horario = models.TimeField()
    alocacao = models.ForeignKey(Alocacao)
    quantidade = models.IntegerField()

class Agente(models.Model):
    SEXO_CHOICES = (
        ('Feminino', 'Feminino'),
        ('Masculino', 'Masculino')
    )

    nome = models.CharField(max_length=200)
    datanascimento = models.DateField()
    sexo = models.CharField(max_length=8, choices=SEXO_CHOICES)
    gritodeduerra = models.CharField(max_length=50)

class Viatura(models.Model):
    numero = models.IntegerField()
    placa = models.CharField(max_length=7)
