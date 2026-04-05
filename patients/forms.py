from django import forms

from .models import Patient, PatientDocument


class NursePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('name', 'age')


class DoctorPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('name', 'age', 'medical_info', 'created_by')


class PatientDocumentForm(forms.ModelForm):
    class Meta:
        model = PatientDocument
        fields = ('title', 'file')
