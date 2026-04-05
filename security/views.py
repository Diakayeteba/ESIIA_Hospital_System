from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import User

from .otp_cookies import clear_otp_pending_cookie, clear_otp_session, get_pending_otp_user_id
from .services import verify_login_otp


@require_http_methods(['GET', 'POST'])
def verify_otp_view(request):
    pending_uid = get_pending_otp_user_id(request)

    if request.user.is_authenticated:
        if pending_uid is None:
            return redirect('accounts:dashboard')
        if request.user.pk == pending_uid:
            return redirect('accounts:dashboard')

    if pending_uid is None:
        messages.warning(request, 'Session expirée. Veuillez vous reconnecter.')
        resp = redirect('accounts:login')
        clear_otp_pending_cookie(resp)
        return resp

    if request.session.get('otp_user_id') != pending_uid:
        request.session['otp_user_id'] = pending_uid

    try:
        user = User.objects.get(pk=pending_uid)
    except User.DoesNotExist:
        clear_otp_session(request)
        resp = redirect('accounts:login')
        clear_otp_pending_cookie(resp)
        return resp

    max_otp = 5
    attempts = int(request.session.get('otp_attempts', 0))
    if attempts >= max_otp:
        messages.error(request, 'Trop de tentatives avec le code. Reconnectez-vous.')
        clear_otp_session(request)
        resp = redirect('accounts:login')
        clear_otp_pending_cookie(resp)
        return resp

    if request.method == 'POST':
        code = (request.POST.get('code') or '').strip()
        if verify_login_otp(user, code):
            login(request, user)
            clear_otp_session(request)
            messages.success(request, 'Double authentification validée. Bienvenue.')
            resp = redirect('accounts:dashboard')
            clear_otp_pending_cookie(resp)
            return resp
        request.session['otp_attempts'] = attempts + 1
        messages.error(request, 'Code incorrect ou expiré.')

    return render(request, 'security/verify_otp.html', {'otp_user': user})
