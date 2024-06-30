from django.db import models

class Jurnal(models.Model):
    nama = models.TextField()
    tanggal = models.DateField()
    skp_tahunan = models.CharField(max_length=100)
    id_regu = models.IntegerField() 
    jurnal_harian = models.TextField()
    jumlah = models.IntegerField()
    satuan = models.CharField(max_length=50)
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    nilai = models.FloatField()
    komentar = models.TextField()
    tanggal_isi = models.DateField()
    lampiran = models.FileField(upload_to='lampiran/', null=True, blank=True)

    class Meta:
        db_table = "jurnal_harian"