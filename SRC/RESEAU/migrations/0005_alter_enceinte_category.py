# Generated by Django 4.1.4 on 2023-02-18 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RESEAU', '0004_remove_patient_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enceinte',
            name='category',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='RESEAU.categorie'),
        ),
    ]
