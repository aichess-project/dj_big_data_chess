# Generated by Django 4.1.5 on 2024-09-04 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0005_rename_zip_sub_folder_folderconfig_big_folder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folderconfig',
            name='unzip_sub_folder',
        ),
        migrations.AddField(
            model_name='folderconfig',
            name='target_folder',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='folderconfig',
            name='big_folder',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='folderconfig',
            name='local_folder',
            field=models.CharField(max_length=64),
        ),
    ]
