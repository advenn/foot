# Generated by Django 4.0.4 on 2022-04-26 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upcoming', '0004_rate_match_rate_predict'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='predict',
        ),
    ]
