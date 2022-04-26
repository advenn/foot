# Generated by Django 4.0.4 on 2022-04-26 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upcoming', '0003_remove_rate_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='match',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='upcoming.upcomingmatch'),
        ),
        migrations.AddField(
            model_name='rate',
            name='predict',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='upcoming.predict'),
        ),
    ]