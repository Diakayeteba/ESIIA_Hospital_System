from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from accounts.decorators import role_required
from accounts.models import User

from .forms import DoctorPatientForm, NursePatientForm, PatientDocumentForm
from .models import Patient, PatientDocument


@role_required(User.Role.NURSE)
@require_http_methods(['GET', 'POST'])
def nurse_patient_create(request):
    if request.method == 'POST':
        form = NursePatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            messages.success(
                request,
                f'Patient enregistré. Identifiant à communiquer au patient : {patient.unique_id}',
            )
            return redirect('patients:nurse_list')
    else:
        form = NursePatientForm()
    return render(request, 'patients/nurse_patient_form.html', {'form': form})


@role_required(User.Role.NURSE)
def nurse_patient_list(request):
    patients_qs = Patient.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'patients/nurse_patient_list.html', {'patients': patients_qs})


@role_required(User.Role.DOCTOR)
def doctor_patient_list(request):
    patients_qs = Patient.objects.select_related('created_by', 'user').order_by('-created_at')
    return render(request, 'patients/doctor_patient_list.html', {'patients': patients_qs})


@role_required(User.Role.DOCTOR)
def doctor_patient_detail(request, pk):
    patient = get_object_or_404(Patient.objects.select_related('created_by', 'user'), pk=pk)
    documents = patient.documents.all()
    return render(
        request,
        'patients/doctor_patient_detail.html',
        {'patient': patient, 'documents': documents},
    )


@role_required(User.Role.DOCTOR)
@require_http_methods(['GET', 'POST'])
def doctor_patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = DoctorPatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dossier patient mis à jour.')
            return redirect('patients:doctor_detail', pk=patient.pk)
    else:
        form = DoctorPatientForm(instance=patient)
    return render(
        request,
        'patients/doctor_patient_form.html',
        {'form': form, 'patient': patient, 'title': 'Modifier le dossier'},
    )


@role_required(User.Role.DOCTOR)
@require_http_methods(['GET', 'POST'])
def doctor_patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient supprimé.')
        return redirect('patients:doctor_list')
    return render(request, 'patients/doctor_patient_confirm_delete.html', {'patient': patient})


@role_required(User.Role.DOCTOR)
@require_http_methods(['GET', 'POST'])
def doctor_document_upload(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    if request.method == 'POST':
        form = PatientDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.patient = patient
            doc.uploaded_by = request.user
            doc.save()
            messages.success(request, 'Document ajouté.')
            return redirect('patients:doctor_detail', pk=patient.pk)
    else:
        form = PatientDocumentForm()
    return render(
        request,
        'patients/document_upload.html',
        {'form': form, 'patient': patient},
    )


@role_required(User.Role.PATIENT)
def patient_documents_list(request):
    profile = getattr(request.user, 'patient_profile', None)
    if profile is None:
        messages.warning(
            request,
            'Votre compte n’est pas encore lié à un dossier. Contactez l’accueil.',
        )
        return render(request, 'patients/patient_documents.html', {'documents': [], 'profile': None})
    documents = PatientDocument.objects.filter(patient=profile).order_by('-uploaded_at')
    return render(
        request,
        'patients/patient_documents.html',
        {'documents': documents, 'profile': profile},
    )
