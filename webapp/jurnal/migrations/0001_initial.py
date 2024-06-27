# Generated by Django 5.0.4 on 2024-06-27 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jurnal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField()),
                ('skp_tahunan', models.CharField(max_length=100)),
                ('id_regu', models.IntegerField()),
                ('jurnal_harian', models.TextField()),
                ('jumlah', models.IntegerField()),
                ('satuan', models.CharField(max_length=50)),
                ('jam_mulai', models.TimeField()),
                ('jam_selesai', models.TimeField()),
                ('nilai', models.FloatField()),
                ('komentar', models.TextField()),
                ('tanggal_isi', models.DateField()),
                ('lampiran', models.FileField(blank=True, null=True, upload_to='lampiran/')),
            ],
            options={
                'db_table': 'jurnal_harian',
            },
        ),
    ]
