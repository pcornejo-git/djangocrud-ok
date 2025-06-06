# Generated by Django 5.2.1 on 2025-05-27 03:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_sucursal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'iom_estatus',
            },
        ),
        migrations.CreateModel(
            name='Hilos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'iom_hilos',
            },
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'iom_personal',
            },
        ),
        migrations.CreateModel(
            name='OrdenFabricacionEnc',
            fields=[
                ('id_orden_fabricacion_enc', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.IntegerField()),
                ('fecha_orden_fabricacion', models.DateField()),
                ('descripcion', models.CharField(max_length=50)),
                ('info_adicional', models.CharField(max_length=100)),
                ('fecha_corte', models.DateField()),
                ('fecha_armado', models.DateField()),
                ('fecha_embalaje', models.DateField()),
                ('activo', models.BooleanField(default=True)),
                ('id_estatus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tasks.estatus')),
                ('id_hilos', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tasks.hilos')),
                ('id_sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tasks.sucursal')),
                ('id_armador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ordenes_armador', to='tasks.personal')),
                ('id_cortador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ordenes_cortador', to='tasks.personal')),
                ('id_empacador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ordenes_empacador', to='tasks.personal')),
                ('id_vendedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ordenes_vendedor', to='tasks.personal')),
            ],
        ),
    ]
