from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        DOCTOR = 'doctor', 'Médecin'
        NURSE = 'nurse', 'Infirmier(e)'
        PATIENT = 'patient', 'Patient'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT,
        verbose_name='rôle',
    )

    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'utilisateur'
        verbose_name_plural = 'utilisateurs'
