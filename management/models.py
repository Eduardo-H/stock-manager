from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Viatura(models.Model):
    numero = models.IntegerField()
    placa = models.CharField(max_length=7)

    def __str__(self):
        return str(self.numero)

class Item(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Agente(models.Model):
    SEXO_CHOICES = (
        ('Feminino', 'Feminino'),
        ('Masculino', 'Masculino')
    )

    nome = models.CharField(max_length=200)
    datanascimento = models.DateField()
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    gritodeguerra = models.CharField(max_length=50)

    def __str__(self):
        return self.gritodeguerra

class Alocacao(models.Model):
    TURNO_CHOICES = (
        ('Manhã', 'Manhã'),
        ('Tarde', 'Tarde'),
        ('Noite', 'Noite'),
        ('Madrugada', 'Madrugada')
    )

    STATUS_CHOICES = (
        ('Aberto', 'Aberto'),
        ('Fechado', 'Fechado'),
        ('Desativado', 'Desativado')
    )

    data = models.DateField()
    horario = models.TimeField()
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES)
    viatura = models.ForeignKey(Viatura, on_delete=models.PROTECT, blank=True, null=True)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=25)
    complemento = models.CharField(max_length=25, blank=True)
    motivo = models.CharField(max_length=100, blank=True)
    cadastrador = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='Fechado')

    def __str__(self):
        return 'Alocação feita no dia {} em {}'.format(self.data, self.rua)

class AlocacaoAgente(models.Model):
    alocacao = models.ForeignKey(Alocacao, on_delete=models.PROTECT)
    agente = models.ForeignKey(Agente, on_delete=models.PROTECT)

    def __str__(self):
        return 'Agente: {}, Data: {}, Local: {}'.format(self.agente.gritodeguerra, self.alocacao.data, self.alocacao.rua)

class Recolhimento(models.Model):
    TURNO_CHOICES = (
        ('Manhã', 'Manhã'),
        ('Tarde', 'Tarde'),
        ('Noite', 'Noite'),
        ('Madrugada', 'Madrugada')
    )

    data = models.DateField()
    horario = models.TimeField()
    quantidade = models.IntegerField()
    alocacao = models.ForeignKey(Alocacao, on_delete=models.PROTECT)
    viatura = models.ForeignKey(Viatura, on_delete=models.PROTECT, blank=True, null=True)
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES)
    cadastrador = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return 'Recolhimento feito no dia {}. Alocação do dia {} em {}'.format(self.data, self.alocacao.rua, self.alocacao.rua)

class RecolhimentoAgente(models.Model):
    recolhimento = models.ForeignKey(Recolhimento, on_delete=models.PROTECT)
    agente = models.ForeignKey(Agente, on_delete=models.PROTECT)

    def __str__(self):
        return 'Agente: {}, Data: {}'.format(self.agente.gritodeguerra, self.recolhimento.data)

class AlocacaoRecolhimento(models.Model):
    alocacao = models.ForeignKey(Alocacao, on_delete=models.PROTECT, blank=True, null=True)
    recolhimento = models.ForeignKey(Recolhimento, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        if self.alocacao is not None:
            return 'Alocação feita no dia {} em {}'.format(self.alocacao.data, self.alocacao.rua)
        else:
            return 'Recolhimento feito no dia {}'.format(self.recolhimento.data)

class Estoque(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantidade = models.IntegerField()

    def __str__(self):
        return self.item.nome

class ItemPerdidoExtraviado(models.Model):
    data = models.DateField()
    horario = models.TimeField()
    alocacao = models.ForeignKey(Alocacao, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
