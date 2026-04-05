from django.conf import settings
from django.db import models


class LoginOTP(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='login_otps',
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'OTP de connexion'
        verbose_name_plural = 'OTP de connexion'

    def __str__(self) -> str:
        return f'{self.user} — {self.code} ({self.created_at})'
