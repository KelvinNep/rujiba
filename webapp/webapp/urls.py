from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views as dashboard_views
from jurnal import views as jurnal_views
from rekapulasi import views as rekapulasi_views
from login import views as login_views
from survey import views as survey_views
from logout import views as logout_views
from dashboard.views import custom_permission_denied_view


# URL patterns
urlpatterns = [
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('proses-data/', dashboard_views.proses_data, name='proses-data'),
    path('survey/', survey_views.survey, name='survey'),
    path('jurnal/', jurnal_views.jurnal, name='jurnal'),  
    path('rekapulasi/', rekapulasi_views.rekapulasi, name='rekapulasi'), 
    path('admin/', login_views.admin_login, name='admin'),
    path('logout/', logout_views.user_logout, name='logout'),
    path('403-forbidden/', custom_permission_denied_view, name='403-forbidden'),

    # URL MAIN ACTION JURNAL
    path('add_jurnal/', jurnal_views.add_jurnal, name='add_jurnal'), 
    path('edit_jurnal/<int:id>/', jurnal_views.edit_jurnal, name='edit_jurnal'),
    path('update_jurnal/<int:id>/', jurnal_views.update_jurnal, name='update_jurnal'),
    path('delete_jurnal/<int:id>/', jurnal_views.delete_jurnal, name='delete_jurnal'),
    path('import_jurnal/', jurnal_views.import_jurnal, name='import_jurnal'),
    path('get_survey/', survey_views.get_survey, name='get_survey'),
    
    # URL MAIN ACTION REKAPULASI
    path('add_rekap/', rekapulasi_views.add_rekap, name='add_rekap'), 
    path('edit_rekap/<int:pk>/', rekapulasi_views.edit_rekap, name='edit_rekap'),
    path('update_rekap/<int:pk>/', rekapulasi_views.update_rekap, name='update_rekap'),
    path('delete_rekap/<int:pk>/', rekapulasi_views.delete_rekap, name='delete_rekap'),
    
    # URL MAIN ACTION SURVEY
    path('add_survey/', survey_views.add_survey, name='add_survey'), 
    path('edit_survey/<int:id>/', survey_views.edit_survey, name='edit_survey'),
    path('update_survey/<int:id>/', survey_views.update_survey, name='update_survey'),
    path('delete_survey/<int:id>/', survey_views.delete_survey, name='delete_survey'),
    
    
]

# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
