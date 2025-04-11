# Generated by Django 5.0.6 on 2025-02-04 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_backend', '0016_alter_pubinfo_data_pub'),
    ]

    operations = [
        migrations.AddField(
            model_name='pubinfo',
            name='tipo_n',
            field=models.CharField(default='Desconhecido', max_length=5),
        ),
        migrations.AlterField(
            model_name='pubinfo',
            name='data_pub',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 4, 13, 47, 5, 221030, tzinfo=datetime.timezone.utc), editable=None),
        ),
    ]
