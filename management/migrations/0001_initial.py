# Generated by Django 2.2.7 on 2020-07-20 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('datanascimento', models.DateField(blank=True, null=True)),
                ('sexo', models.CharField(choices=[('Feminino', 'Feminino'), ('Masculino', 'Masculino')], max_length=10)),
                ('gritodeguerra', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Alocacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('horario', models.TimeField()),
                ('quantidade', models.IntegerField()),
                ('turno', models.CharField(choices=[('Manhã', 'Manhã'), ('Tarde', 'Tarde'), ('Noite', 'Noite'), ('Madrugada', 'Madrugada')], max_length=10)),
                ('rua', models.CharField(max_length=200)),
                ('numero', models.CharField(max_length=10)),
                ('bairro', models.CharField(max_length=25)),
                ('complemento', models.CharField(blank=True, max_length=25)),
                ('motivo', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('Aberto', 'Aberto'), ('Fechado', 'Fechado'), ('Desativado', 'Desativado')], default='Fechado', max_length=11)),
                ('cadastrador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Recolhimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('horario', models.TimeField()),
                ('quantidade', models.IntegerField()),
                ('turno', models.CharField(choices=[('Manhã', 'Manhã'), ('Tarde', 'Tarde'), ('Noite', 'Noite'), ('Madrugada', 'Madrugada')], max_length=10)),
                ('alocacao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Alocacao')),
                ('cadastrador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Viatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('placa', models.CharField(blank=True, default='-', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='RecolhimentoAgente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Agente')),
                ('recolhimento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Recolhimento')),
            ],
        ),
        migrations.AddField(
            model_name='recolhimento',
            name='viatura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='management.Viatura'),
        ),
        migrations.CreateModel(
            name='ItemPerdidoExtraviado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('horario', models.TimeField()),
                ('quantidade', models.IntegerField()),
                ('alocacao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Alocacao')),
            ],
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Item')),
            ],
        ),
        migrations.CreateModel(
            name='AlocacaoRecolhimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alocacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='management.Alocacao')),
                ('recolhimento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='management.Recolhimento')),
            ],
        ),
        migrations.CreateModel(
            name='AlocacaoAgente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Agente')),
                ('alocacao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Alocacao')),
            ],
        ),
        migrations.AddField(
            model_name='alocacao',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Item'),
        ),
        migrations.AddField(
            model_name='alocacao',
            name='viatura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='management.Viatura'),
        ),
    ]
