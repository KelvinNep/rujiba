from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import JurnalForm, UploadFileForm
from .models import Jurnal
import pandas as pd

@never_cache
@login_required
def jurnal(request):
    jurnals = Jurnal.objects.all()
    return render(request, 'jurnal.html', {'jurnals': jurnals})

@login_required
def add_jurnal(request):
    if request.method == 'POST':
        form = JurnalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('jurnal')
    else:
        form = JurnalForm()
    return render(request, 'add_jurnal.html', {'form': form})

@login_required
def edit_jurnal(request, id):  
    jurnal = get_object_or_404(Jurnal, id=id)
    jurnal_data = {
        'id': jurnal.id,
        'nama': jurnal.nama,
        'tanggal': jurnal.tanggal,
        'skp_tahunan': jurnal.skp_tahunan,
        'id_regu': jurnal.id_regu,
        'jurnal_harian': jurnal.jurnal_harian,
        'jumlah': jurnal.jumlah,
        'satuan': jurnal.satuan,
        'jam_mulai': jurnal.jam_mulai,
        'jam_selesai': jurnal.jam_selesai,
        'nilai': jurnal.nilai,
        'komentar': jurnal.komentar,
        'tanggal_isi': jurnal.tanggal_isi,
    }
    return JsonResponse(jurnal_data) 

@login_required
def update_jurnal(request, id):  
    jurnal = get_object_or_404(Jurnal, id=id)
    if request.method == 'POST':
        form = JurnalForm(request.POST, instance=jurnal)
        if form.is_valid():
            form.save()
            return redirect('jurnal')
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        form = JurnalForm(instance=jurnal)
    return render(request, 'edit_jurnal.html', {'form': form, 'jurnal': jurnal})

@login_required
def delete_jurnal(request, id):
    jurnal = get_object_or_404(Jurnal, id=id)
    jurnal.delete()
    return redirect('jurnal')

@login_required
def import_jurnal(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_extension = file.name.split('.')[-1].lower()
            
            # Memilih engine berdasarkan ekstensi file
            if file_extension in ['xlsx', 'xls', 'xlsm']:
                engine = 'openpyxl'
            else:
                return HttpResponse("Unsupported file format", status=400)

            try:
                # Membaca file Excel
                df = pd.read_excel(file, engine=engine)
            except Exception as e:
                return HttpResponse(f"Error reading the file: {str(e)}", status=400)

            try:
                # Memproses data dari dataframe sesuai kebutuhan Anda
                for _, row in df.iterrows():
                    Jurnal.objects.create(
                        tanggal=row['Tanggal'],
                        skp_tahunan=row['SKP Tahunan'],
                        id_regu=row['id_regu'],
                        jurnal_harian=row['Jurnal Harian'],
                        jumlah=row['Jumlah'],
                        satuan=row['Satuan'],
                        jam_mulai=row['Jam Mulai'],
                        jam_selesai=row['Jam Selesai'],
                        nilai=row['Nilai'],
                        komentar=row['Komentar'],
                        tanggal_isi=row['Tanggal Isi']
                    )
            except KeyError as e:
                return HttpResponse(f"Missing column in the file: {str(e)}", status=400)
            except Exception as e:
                return HttpResponse(f"Error processing the file: {str(e)}", status=400)

            return HttpResponse("File uploaded and processed successfully!")
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
