# Generated by Django 5.1.4 on 2025-01-21 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_backend', '0008_rename_test_hash_user_info_enctype_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_complemento',
            name='cep',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='user_complemento',
            name='cpf',
            field=models.CharField(blank=True, max_length=11),
        ),
        migrations.AlterField(
            model_name='user_complemento',
            name='date',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user_complemento',
            name='endereco',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='user_complemento',
            name='estado',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='user_complemento',
            name='numero',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='user_complemento',
            name='rua',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
