"""Cookie signé pour le flux OTP : reste valide même si une autre connexion modifie la session / le jeton CSRF."""

from django.conf import settings
from django.core.signing import BadSignature
from django.http import HttpResponse


def _cookie_name() -> str:
    return getattr(settings, 'EHS_OTP_PENDING_COOKIE', 'ehs_otp_pending')


def _salt() -> str:
    return getattr(settings, 'EHS_OTP_PENDING_SALT', 'ehs.security.otp.v1')


def _max_age() -> int:
    return int(getattr(settings, 'OTP_VALIDITY_MINUTES', 10)) * 60


def attach_otp_pending_cookie(response: HttpResponse, user_pk: int) -> HttpResponse:
    response.set_signed_cookie(
        _cookie_name(),
        str(int(user_pk)),
        salt=_salt(),
        max_age=_max_age(),
        httponly=True,
        samesite='Lax',
        path='/',
    )
    return response


def clear_otp_pending_cookie(response: HttpResponse) -> HttpResponse:
    response.delete_cookie(_cookie_name(), path='/', samesite='Lax')
    return response


def get_pending_otp_user_id(request) -> int | None:
    uid = request.session.get('otp_user_id')
    if uid is not None:
        try:
            return int(uid)
        except (TypeError, ValueError):
            pass
    try:
        raw = request.get_signed_cookie(_cookie_name(), salt=_salt(), max_age=_max_age())
        return int(raw)
    except (KeyError, BadSignature, ValueError, TypeError):
        return None


def clear_otp_session(request) -> None:
    request.session.pop('otp_user_id', None)
    request.session.pop('otp_attempts', None)
