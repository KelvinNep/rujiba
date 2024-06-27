from django import forms
from .models import Rekapulasi

class RekapulasiForm(forms.ModelForm):
    class Meta:
        model = Rekapulasi
        fields = ['nip', 'nama', 'id_regu', 'unit_kerja', 'terlambat', 'pulang_cepat', 'terlambat_menit', 'pulang_cepat_menit', 'tanpa_keterangan', 'terlambat_izin', 'pulang_cepat_izin', 'lupa_absen_masuk', 'lupa_absen_pulang', 'full', 'half', 'total']

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Pilih File Excel (.xlsx, .xls, .csv, .xlsm)')
    