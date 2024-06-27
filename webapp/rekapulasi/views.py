from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import RekapulasiForm, UploadFileForm
from .models import Rekapulasi
import pandas as pd
from django.core.cache import cache
cache.clear()

@never_cache
@login_required
def rekapulasi(request):
    rekap = Rekapulasi.objects.all()
    return render(request, 'rekapulasi.html', {'rekap': rekap})

@login_required
def add_rekap(request):
    if request.method == 'POST':
        form = RekapulasiForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('rekapulasi')
    else:
        form = RekapulasiForm()
    return render(request, 'add_rekapulasi.html', {'form': form})

@login_required
def edit_rekap(request, pk):  
    rekap = get_object_or_404(Rekapulasi, id=pk)
    rekap_data = {
        'nip': rekap.nip,
        'nama': rekap.nama,
        'unit_kerja': rekap.unit_kerja,
        'id_regu' : rekap.id_regu,
        'terlambat': rekap.terlambat,
        'pulang_cepat': rekap.pulang_cepat,
        'terlambat_menit': rekap.terlambat_menit,
        'pulang_cepat_menit': rekap.pulang_cepat_menit,
        'tanpa_keterangan': rekap.tanpa_keterangan,
        'terlambat_izin': rekap.terlambat_izin,
        'pulang_cepat_izin': rekap.pulang_cepat_izin,
        'lupa_absen_masuk': rekap.lupa_absen_masuk,
        'lupa_absen_pulang': rekap.lupa_absen_pulang,
        'full': rekap.full,
        'half': rekap.half,
        'total': rekap.total,
    }
    return JsonResponse(rekap_data) 

@login_required
def update_rekap(request, pk):  
    rekap = get_object_or_404(Rekapulasi, id=pk)
    if request.method == 'POST':
        form = RekapulasiForm(request.POST, instance=rekap)
        if form.is_valid():
            form.save()
            return redirect('rekapulasi')
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        form = RekapulasiForm(instance=rekap)
    return render(request, 'edit_rekapulasi.html', {'form': form, 'rekap': rekap})

@login_required
def delete_rekap(request, pk):
    rekap = get_object_or_404(Rekapulasi, id=pk)
    rekap.delete()
    return redirect('rekapulasi')