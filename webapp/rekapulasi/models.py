from django.db import models

class Rekapulasi(models.Model):
    nip = models.CharField(max_length=20)
    nama = models.CharField(max_length=255)
    unit_kerja = models.CharField(max_length=255)
    id_regu = models.IntegerField()
    terlambat = models.IntegerField(default=0)
    pulang_cepat = models.IntegerField(default=0)
    terlambat_menit = models.IntegerField(default=0)
    pulang_cepat_menit = models.IntegerField(default=0)
    tanpa_keterangan = models.IntegerField(default=0)
    terlambat_izin = models.IntegerField(default=0)
    pulang_cepat_izin = models.IntegerField(default=0)
    lupa_absen_masuk = models.IntegerField(default=0)
    lupa_absen_pulang = models.IntegerField(default=0)
    full = models.IntegerField(default=0)
    half = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    class Meta:
        db_table = "rekapulasi"
