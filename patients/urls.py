from django.urls import path

from . import views

app_name = 'patients'

urlpatterns = [
    path('infirmier/nouveau/', views.nurse_patient_create, name='nurse_create'),
    path('infirmier/liste/', views.nurse_patient_list, name='nurse_list'),
    path('medecin/liste/', views.doctor_patient_list, name='doctor_list'),
    path('medecin/<int:pk>/', views.doctor_patient_detail, name='doctor_detail'),
    path('medecin/<int:pk>/modifier/', views.doctor_patient_edit, name='doctor_edit'),
    path('medecin/<int:pk>/supprimer/', views.doctor_patient_delete, name='doctor_delete'),
    path(
        'medecin/<int:patient_pk>/document/',
        views.doctor_document_upload,
        name='doctor_document_upload',
    ),
    path('patient/mes-documents/', views.patient_documents_list, name='patient_documents'),
]
