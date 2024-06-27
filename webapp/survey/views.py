from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import SurveyForm, UploadFileForm
from .models import Survey
import pandas as pd

# Create your views here.
@never_cache
@login_required
def survey(request):
    survey = Survey.objects.all()
    return render(request, 'survey.html', {'survey': survey})

@login_required
def add_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('survey')
    else:
        form = SurveyForm()
    return render(request, 'add_survey.html', {'form': form})

@login_required
def edit_survey(request, id):  
    survey = get_object_or_404(Survey, id=id)
    survey_data = {
        'id': survey.id,
        'nama': survey.nama,
        'pertanyaan1': survey.pertanyaan1,
        'pertanyaan2': survey.pertanyaan2,
    }
    return JsonResponse(survey_data) 

@login_required
def update_survey(request, id):  
    survey = get_object_or_404(Survey, id=id)
    if request.method == 'POST':
        form = SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect('survey')
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        form = SurveyForm(instance=survey)
    return render(request, 'edit_survey.html', {'form': form, 'survey': survey})

@login_required
def delete_survey(request, id):
    survey = get_object_or_404(Survey, id=id)
    survey.delete()
    return redirect('survey')

@login_required
def get_survey(request):
    surveys = Survey.objects.all().values('id', 'nama')
    surveys_list = list(surveys)
    return JsonResponse(surveys_list, safe=False)