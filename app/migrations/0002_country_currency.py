# Generated by Django 3.2 on 2022-11-22 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='currency',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='العملة'),
        ),
    ]
