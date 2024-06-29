from django.db import models
from django.db.models import Avg

class Regu(models.Model):
    nama = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nama

class Rekapitulasi(models.Model):
    nip = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=255)
    unit_kerja = models.CharField(max_length=255)
    regu = models.ForeignKey(Regu, on_delete=models.CASCADE)
    terlambat = models.IntegerField()
    pulang_cepat = models.IntegerField()
    terlambat_menit = models.IntegerField()
    pulang_cepat_menit = models.IntegerField()
    tanpa_keterangan = models.IntegerField()
    terlambat_izin = models.IntegerField()
    pulang_cepat_izin = models.IntegerField()
    lupa_absen_masuk = models.IntegerField()
    lupa_absen_pulang = models.IntegerField()
    full = models.IntegerField()
    half = models.IntegerField()
    total = models.IntegerField()

class JurnalHarian(models.Model):
    nama = models.TextField()
    tanggal = models.DateField()
    skp_tahunan = models.CharField(max_length=100)
    regu = models.ForeignKey(Regu, on_delete=models.CASCADE)
    jurnal_harian = models.TextField()
    jumlah = models.IntegerField()
    satuan = models.CharField(max_length=50)
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    nilai = models.FloatField()
    komentar = models.TextField()
    tanggal_isi = models.DateField()
    lampiran = models.CharField(max_length=100, null=True, blank=True)

class Survey(models.Model):
    regu = models.ForeignKey(Regu, on_delete=models.CASCADE)
    point_regu = models.IntegerField()

class Penilaian(models.Model):
    regu = models.ForeignKey(Regu, on_delete=models.CASCADE)
    nilai_absen = models.FloatField()
    nilai_jurnal = models.FloatField()
    nilai_kuisioner = models.FloatField()
    status = models.CharField(max_length=50, null=True, blank=True)

    @classmethod
    def create_data_testing(cls):
        data_testing_list = []
        regus = Regu.objects.all()
        for regu in regus:
            nilai_absen = Rekapitulasi.objects.filter(regu=regu).aggregate(
                average_nilai_absen=Avg(100 - models.F('total'))
            )['average_nilai_absen']

            nilai_jurnal = JurnalHarian.objects.filter(regu=regu).aggregate(
                average_nilai_jurnal=Avg('nilai')
            )['average_nilai_jurnal']

            nilai_kuisioner = Survey.objects.filter(regu=regu).aggregate(
                average_nilai_kuisioner=Avg('point_regu')
            )['average_nilai_kuisioner']

            data_testing = cls(
                regu=regu,
                nilai_absen=nilai_absen if nilai_absen is not None else 0,
                nilai_jurnal=nilai_jurnal if nilai_jurnal is not None else 0,
                nilai_kuisioner=nilai_kuisioner if nilai_kuisioner is not None else 0,
                status=''
            )
            data_testing_list.append(data_testing)
        
        cls.objects.bulk_create(data_testing_list)

class HasilPrediksi(models.Model):
    regu = models.ForeignKey(Regu, on_delete=models.CASCADE)
    penilaian = models.ForeignKey(Penilaian, on_delete=models.CASCADE)
    predicted_status = models.CharField(max_length=50)
    prediction_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prediksi untuk {self.regu.nama} - Status: {self.predicted_status}"