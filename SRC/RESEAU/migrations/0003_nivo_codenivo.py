# Generated by Django 4.1.4 on 2023-02-16 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RESEAU', '0002_rename_nonreso_reso_nomreso_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nivo',
            name='codenivo',
            field=models.CharField(default='FS', max_length=2),
        ),
    ]
