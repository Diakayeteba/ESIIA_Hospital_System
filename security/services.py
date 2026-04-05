import secrets
import string
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import LoginOTP


def _generate_code(length: int = 6) -> str:
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def _otp_created_at_aware(otp: LoginOTP):
    """Garantit une datetime comparable avec timezone.now() (cas SQLite / fuseaux)."""
    created = otp.created_at
    if timezone.is_naive(created):
        return timezone.make_aware(created, timezone.get_current_timezone())
    return created


def _debug_log_otp(user, code: str) -> None:
    if not getattr(settings, 'DEBUG', False):
        return
    msg = f'[EHS OTP] compte={user.get_username()} code={code}'
    print(f'\n{msg}\n', flush=True)
    # Fichier à la racine du projet (pratique si le terminal Cursor n’affiche pas tout)
    try:
        log_path = settings.BASE_DIR / 'ehs_otp_debug.log'
        line = f'{timezone.now().isoformat(sep=" ", timespec="seconds")} | {msg}\n'
        with open(log_path, 'a', encoding='utf-8') as fh:
            fh.write(line)
    except OSError:
        pass


def _normalize_otp_code(raw: str) -> str:
    """Ne garde que les chiffres (coller depuis la console / SMS sans espaces parasites)."""
    if not raw:
        return ''
    return ''.join(ch for ch in raw.strip() if ch.isdigit())


def issue_login_otp(user) -> str:
    """
    Crée un OTP ou réutilise le dernier encore valide et récent (voir OTP_REUSE_WINDOW_SECONDS).
    Évite qu’un second POST sur « Connexion » invalide le code déjà affiché dans la console.
    """
    reuse_seconds = int(getattr(settings, 'OTP_REUSE_WINDOW_SECONDS', 300))
    window_start = timezone.now() - timedelta(seconds=reuse_seconds)

    existing = (
        LoginOTP.objects.filter(user=user, is_valid=True, created_at__gte=window_start)
        .order_by('-created_at')
        .first()
    )
    if existing is not None:
        _debug_log_otp(user, existing.code)
        return existing.code

    LoginOTP.objects.filter(user=user, is_valid=True).update(is_valid=False)
    code = _generate_code()
    LoginOTP.objects.create(user=user, code=code, is_valid=True)
    subject = 'EHS — Code de vérification'
    body = (
        f'Bonjour {user.get_username()},\n\n'
        f'Votre code de double authentification est : {code}\n'
        f'Il expire dans {getattr(settings, "OTP_VALIDITY_MINUTES", 10)} minutes.\n'
    )
    if user.email:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
    _debug_log_otp(user, code)
    return code


def verify_login_otp(user, code: str) -> bool:
    normalized = _normalize_otp_code(code)
    if not normalized:
        return False

    otp = (
        LoginOTP.objects.filter(user=user, is_valid=True)
        .order_by('-created_at')
        .first()
    )
    if otp is None:
        return False

    validity = timedelta(minutes=getattr(settings, 'OTP_VALIDITY_MINUTES', 10))
    created = _otp_created_at_aware(otp)
    if created < timezone.now() - validity:
        return False

    if len(normalized) != len(otp.code):
        return False
    if not secrets.compare_digest(otp.code, normalized):
        return False

    otp.is_valid = False
    otp.save(update_fields=['is_valid'])
    return True
