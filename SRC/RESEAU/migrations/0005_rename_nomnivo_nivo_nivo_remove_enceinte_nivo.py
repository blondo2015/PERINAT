# Generated by Django 4.1.4 on 2023-01-07 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RESEAU', '0004_enceinte_nivo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nivo',
            old_name='nomNivo',
            new_name='nivo',
        ),
        migrations.RemoveField(
            model_name='enceinte',
            name='nivo',
        ),
    ]