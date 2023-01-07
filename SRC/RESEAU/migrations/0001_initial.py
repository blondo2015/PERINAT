# Generated by Django 4.1.4 on 2023-01-07 10:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('mvt_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Enceinte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=10)),
                ('nomEnceinte', models.CharField(max_length=100)),
                ('adresse', models.CharField(default='', max_length=250)),
                ('contact1', models.CharField(default='', max_length=13)),
                ('contact2', models.CharField(default='', max_length=13)),
                ('mvt_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('category', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='RESEAU.categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Equipement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomEquip', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Nivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomNivo', models.CharField(default='FOSA', max_length=50)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nompatient', models.CharField(max_length=250)),
                ('dtenaiss', models.DateField(blank=True, null=True)),
                ('lieunaiss', models.CharField(default='', max_length=100, null=True)),
                ('poids', models.DecimalField(decimal_places=2, max_digits=5)),
                ('petitpoids', models.BooleanField(default=False)),
                ('pathologie', models.CharField(max_length=250)),
                ('sexe', models.CharField(choices=[('F', 'F'), ('M', 'M')], default='F', max_length=150)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Referer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dterefencement', models.DateField(default='')),
                ('mvt_at', models.DateTimeField(auto_now_add=True)),
                ('caregiven', models.CharField(default='', max_length=150)),
                ('transport', models.CharField(choices=[('AMBULANCE', 'AMBULANCE'), ('VEHICULE PERSONNEL', 'VEHICULE PERSONNEL'), ('TRANSPORT EN COMMUN', 'TRANSPORT EN COMMUN'), ('AUTRE MOYEN', 'AUTRE MOYEN')], default='AUTRE MOYEN', max_length=150)),
                ('detailtransport', models.CharField(choices=[('AMBULANCE', 'AMBULANCE'), ('VEHICULE PERSONNEL', 'VEHICULE PERSONNEL'), ('TRANSPORT EN COMMUN', 'TRANSPORT EN COMMUN'), ('AUTRE MOYEN', 'AUTRE MOYEN')], default='', max_length=150)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Reso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nonreso', models.CharField(default='CENTRE', max_length=50)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Secteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomSecteur', models.CharField(default='PUBLIC', max_length=50)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nom', models.CharField(default='', max_length=150)),
                ('telephone', models.CharField(max_length=9, unique=True)),
                ('dteEnrollement', models.DateField(blank=True, null=True)),
                ('sexe', models.CharField(choices=[('F', 'F'), ('M', 'M')], default='F', max_length=150)),
                ('foto', models.ImageField(blank=True, default='', null=True, upload_to='user/')),
                ('mvt_at', models.DateTimeField(auto_now_add=True)),
                ('suspendu', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modify_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objets', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomService', models.CharField(default='NeoNat', max_length=10)),
                ('cautionAdminission', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('enceinte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RESEAU.enceinte')),
            ],
        ),
        migrations.CreateModel(
            name='EquipService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pu', models.FloatField(default=0)),
                ('periodicite', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('equipement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RESEAU.equipement')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RESEAU.service')),
            ],
        ),
        migrations.CreateModel(
            name='EncUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pointfocal', models.BooleanField(default=False)),
                ('dte', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('enceinte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RESEAU.enceinte')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='enceinte',
            name='nivo',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='RESEAU.nivo'),
        ),
        migrations.AddField(
            model_name='enceinte',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RESEAU.enceinte'),
        ),
        migrations.AddField(
            model_name='enceinte',
            name='reso',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='RESEAU.reso'),
        ),
        migrations.AddField(
            model_name='enceinte',
            name='secteur',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='RESEAU.secteur'),
        ),
    ]
