import re

from django.core.exceptions import ValidationError


class HospitalPasswordValidator:
    """Politique EHS : ≥10 caractères, majuscule, minuscule, chiffre, caractère spécial (@, !, $)."""

    pattern_special = re.compile(r'[@!$]')

    def validate(self, password, user=None):
        if len(password) < 10:
            raise ValidationError(
                'Le mot de passe doit contenir au moins 10 caractères.',
                code='password_too_short',
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins une lettre majuscule (A-Z).',
                code='password_no_upper',
            )
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins une lettre minuscule (a-z).',
                code='password_no_lower',
            )
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins un chiffre.',
                code='password_no_digit',
            )
        if not self.pattern_special.search(password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins un caractère spécial parmi : @, !, $.',
                code='password_no_special',
            )

    def get_help_text(self):
        return (
            'Au moins 10 caractères, une majuscule, une minuscule, un chiffre '
            'et un caractère spécial parmi @, !, $.'
        )
