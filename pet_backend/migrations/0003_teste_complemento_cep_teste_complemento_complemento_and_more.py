# Generated by Django 4.2.6 on 2024-12-16 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_backend', '0002_teste_complemento'),
    ]

    operations = [
        migrations.AddField(
            model_name='teste_complemento',
            name='cep',
            field=models.CharField(blank=None, default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teste_complemento',
            name='complemento',
            field=models.CharField(default='desconhecido', max_length=50),
        ),
        migrations.AddField(
            model_name='teste_complemento',
            name='cpf',
            field=models.CharField(blank=None, default=0, max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teste_complemento',
            name='date',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teste_complemento',
            name='endereco',
            field=models.CharField(blank=None, default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teste_complemento',
            name='estado',
            field=models.CharField(blank=None, default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teste_complemento',
            name='id_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teste_complemento',
            name='numero',
            field=models.IntegerField(blank=None, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teste_complemento',
            name='rua',
            field=models.CharField(blank=None, default=0, max_length=50),
            preserve_default=False,
        ),
    ]
