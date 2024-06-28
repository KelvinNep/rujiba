from django import forms
from .models import Jurnal

class JurnalForm(forms.ModelForm):
    class Meta:
        model = Jurnal
        fields = ['id', 'nama', 'tanggal', 'skp_tahunan', 'id_regu', 'jurnal_harian', 'jumlah', 'satuan', 'jam_mulai', 'jam_selesai', 'lampiran', 'nilai', 'komentar', 'tanggal_isi']

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Pilih File Excel (.xlsx, .xls, .csv, .xlsm)')