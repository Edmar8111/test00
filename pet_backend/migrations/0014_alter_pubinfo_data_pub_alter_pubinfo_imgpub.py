# Generated by Django 5.1 on 2025-01-28 19:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet_backend', '0013_alter_pubinfo_data_pub_alter_pubinfo_imgpub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pubinfo',
            name='data_pub',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 28, 19, 47, 17, 708602, tzinfo=datetime.timezone.utc), editable=None),
        ),
        migrations.AlterField(
            model_name='pubinfo',
            name='imgpub',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
