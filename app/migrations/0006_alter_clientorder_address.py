# Generated by Django 3.2 on 2022-12-08 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_address_neighborhood'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientorder',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='addresses', to='app.address', verbose_name='العنوان'),
        ),
    ]