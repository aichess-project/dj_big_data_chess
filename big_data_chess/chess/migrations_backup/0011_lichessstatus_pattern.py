# Generated by Django 4.1.5 on 2024-09-04 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0010_alter_lichessstatus_options_lichessstatus_base_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='lichessstatus',
            name='pattern',
            field=models.CharField(default='lichess_db_standard_rated_<YEAR>-<MONTH>.pgn.zst', max_length=32),
        ),
    ]
