# Generated by Django 5.0.6 on 2025-01-21 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_backend', '0003_teste_complemento_cep_teste_complemento_complemento_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='teste_ong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_id', models.IntegerField(default=0)),
                ('cnpj', models.CharField(blank=None, max_length=11)),
                ('date', models.CharField(max_length=10)),
                ('cep', models.CharField(blank=None, max_length=10)),
                ('estado', models.CharField(blank=None, max_length=50)),
                ('endereco', models.CharField(blank=None, max_length=50)),
                ('rua', models.CharField(blank=None, max_length=50)),
                ('numero', models.IntegerField(blank=None)),
                ('complemento', models.CharField(default='desconhecido', max_length=50)),
            ],
        ),
        migrations.RenameModel(
            old_name='teste',
            new_name='user_info',
        ),
    ]
