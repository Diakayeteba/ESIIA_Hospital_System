import secrets
import string

from django.conf import settings
from django.db import models


def _random_patient_id_segment(length: int = 10) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class Patient(models.Model):
    unique_id = models.CharField(
        max_length=32,
        unique=True,
        editable=False,
        verbose_name='identifiant unique',
    )
    name = models.CharField(max_length=255, verbose_name='nom')
    age = models.PositiveSmallIntegerField(verbose_name='âge')
    medical_info = models.TextField(blank=True, verbose_name='informations médicales')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='patients_created',
        limit_choices_to={'role': 'nurse'},
        verbose_name='enregistré par (infirmier·e)',
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patient_profile',
        limit_choices_to={'role': 'patient'},
        verbose_name='compte patient',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='créé le')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'patient'
        verbose_name_plural = 'patients'

    def __str__(self) -> str:
        return f'{self.name} ({self.unique_id})'

    def save(self, *args, **kwargs):
        if not self.unique_id:
            candidate = f'EHS-{_random_patient_id_segment()}'
            while Patient.objects.filter(unique_id=candidate).exists():
                candidate = f'EHS-{_random_patient_id_segment()}'
            self.unique_id = candidate
        super().save(*args, **kwargs)


class PatientDocument(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='patient',
    )
    title = models.CharField(max_length=255, verbose_name='titre')
    file = models.FileField(upload_to='patient_docs/%Y/%m/', verbose_name='fichier')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='envoyé le')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents_uploaded',
        verbose_name='ajouté par',
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'document patient'
        verbose_name_plural = 'documents patients'

    def __str__(self) -> str:
        return self.title
