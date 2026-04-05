from django import forms
from django.contrib.auth.forms import UserCreationForm

from patients.models import Patient

from .models import User


class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Adresse e-mail')
    patient_unique_id = forms.CharField(
        max_length=32,
        label='Identifiant patient (fourni par l’hôpital)',
        help_text='L’identifiant indiqué sur votre dossier après enregistrement par un infirmier.',
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = (
            'Au moins 10 caractères, majuscule, minuscule, chiffre et un caractère parmi @, !, $.'
        )

    def clean_patient_unique_id(self):
        raw = self.cleaned_data['patient_unique_id'].strip()
        try:
            patient = Patient.objects.get(unique_id__iexact=raw)
        except Patient.DoesNotExist as exc:
            raise forms.ValidationError(
                'Aucun dossier patient ne correspond à cet identifiant.'
            ) from exc
        if patient.user_id is not None:
            raise forms.ValidationError('Ce dossier est déjà associé à un compte.')
        self._linked_patient = patient
        return patient.unique_id

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = User.Role.PATIENT
        if commit:
            user.save()
            patient = getattr(self, '_linked_patient', None)
            if patient:
                patient.user = user
                patient.save(update_fields=['user'])
        return user


class StaffUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['role'].choices = [
            c for c in User.Role.choices if c[0] in (User.Role.DOCTOR, User.Role.NURSE)
        ]
        if self.instance.pk:
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    def clean(self):
        data = super().clean()
        p1 = data.get('password1')
        p2 = data.get('password2')
        if not self.instance.pk:
            if not p1 or not p2:
                raise forms.ValidationError('Le mot de passe est obligatoire pour un nouveau compte.')
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError('Les deux mots de passe ne correspondent pas.')
        return data

    def clean_role(self):
        role = self.cleaned_data['role']
        if role not in (User.Role.DOCTOR, User.Role.NURSE):
            raise forms.ValidationError('Seuls médecin et infirmier peuvent être gérés ici.')
        return role

    def save(self, commit=True):
        user = super().save(commit=False)
        p1 = self.cleaned_data.get('password1')
        if p1:
            user.set_password(p1)
        if commit:
            user.save()
        return user
