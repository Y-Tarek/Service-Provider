# Generated by Django 3.2 on 2022-12-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20221123_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='neighborhood',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='الحى'),
        ),
    ]
