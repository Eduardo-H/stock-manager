from django.db import models
from django.contrib.auth.models import User


class Viatura(models.Model):
    numero = models.IntegerField()
    placa = models.CharField(max_length=7)

class Item(models.Model):
    nome = models.CharField(max_length=100)

class Agente(models.Model):
    SEXO_CHOICES = (
        ('Feminino', 'Feminino'),
        ('Masculino', 'Masculino')
    )

    nome = models.CharField(max_length=200)
    datanascimento = models.DateField()
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    gritodeduerra = models.CharField(max_length=50)

class Alocacao(models.Model):
    TURNO_CHOICES = (
        ('Manhã', 'Manhã'),
        ('Tarde', 'Tarde'),
        ('Noite', 'Noite'),
        ('Madrugada', 'Madrugada')
    )

    data = models.DateField()
    horario = models.TimeField()
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES)
    viatura = models.ForeignKey(Viatura, on_delete=models.PROTECT, blank=True)
    local = models.CharField(max_length=250)
    motivo = models.CharField(max_length=100, blank=True)
    cadastrador = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return 'Alocação feita no dia' + self.data + ' em ' + self.local

class AlocacaoAgente(models.Model):
    alocacao = models.ForeignKey(Alocacao, on_delete=models.PROTECT)
    agente = models.ForeignKey(Agente, on_delete=models.PROTECT)

class Recolhimento(models.Model):
    data = models.DateField()
    horario = models.TimeField()
    alocacao = models.ForeignKey(Alocacao, on_delete=models.PROTECT)
    cadastrador = models.ForeignKey(User, on_delete=models.PROTECT)

class RecolhimentoAgente(models.Model):
    recolhimento = models.ForeignKey(Recolhimento, on_delete=models.PROTECT)
    agente = models.ForeignKey(Agente, on_delete=models.PROTECT)

class AlocacaoRecolhimento(models.Model):
    data = models.DateField()
    horario = models.TimeField()
    alocacao = models.ForeignKey(Alocacao, on_delete=models.PROTECT, blank=True)
    recolhimento = models.ForeignKey(Recolhimento, on_delete=models.PROTECT, blank=True)



class Estoque(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantidade = models.IntegerField()

class ItemPerdidoExtraviado(models.Model):
    data = models.DateField()
    horario = models.TimeField()
    alocacao = models.ForeignKey(Alocacao, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
