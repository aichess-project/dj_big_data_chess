# Generated by Django 4.1.5 on 2024-09-04 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0012_alter_lichessstatus_pattern'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_year', models.SmallIntegerField()),
                ('last_month', models.SmallIntegerField()),
            ],
        ),
    ]
