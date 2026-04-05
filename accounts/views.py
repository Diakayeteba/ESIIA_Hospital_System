from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from security.otp_cookies import attach_otp_pending_cookie, clear_otp_pending_cookie, clear_otp_session
from security.services import issue_login_otp

from .forms import PatientRegistrationForm
from .login_throttle import clear_login_throttle, is_username_locked, register_failed_attempt
from .models import User


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''

        if is_username_locked(username):
            messages.error(
                request,
                'Trop de tentatives. Réessayez plus tard ou contactez l’administration.',
            )
            return render(request, 'accounts/login.html')

        user = authenticate(request, username=username, password=password)
        if user is None:
            register_failed_attempt(username)
            messages.error(request, 'Identifiant ou mot de passe incorrect.')
            return render(request, 'accounts/login.html')

        clear_login_throttle(username)
        issue_login_otp(user)
        request.session['otp_user_id'] = user.pk
        messages.info(
            request,
            'Un code de vérification a été envoyé à votre adresse e-mail. En développement, '
            'regardez aussi la ligne [EHS OTP] dans la console du serveur.',
        )
        response = redirect('security:verify_otp')
        attach_otp_pending_cookie(response, user.pk)
        return response

    return render(request, 'accounts/login.html')


@require_http_methods(['GET', 'POST'])
def register_patient_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Compte créé. Connectez-vous avec le code reçu par e-mail après saisie du mot de passe.',
            )
            return redirect('accounts:login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(['POST'])
def logout_view(request):
    clear_otp_session(request)
    logout(request)
    messages.info(request, 'Vous êtes déconnecté.')
    response = redirect(settings.LOGOUT_REDIRECT_URL)
    clear_otp_pending_cookie(response)
    return response


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    user = request.user
    if user.is_superuser or user.role == User.Role.DOCTOR:
        template = 'dashboard/doctor.html'
    elif user.role == User.Role.NURSE:
        template = 'dashboard/nurse.html'
    else:
        template = 'dashboard/patient.html'
    ctx = {'patient_profile': getattr(request.user, 'patient_profile', None)}
    return render(request, template, ctx)


class EhsPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.txt'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
