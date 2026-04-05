from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = 'accounts'

urlpatterns = [
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
    path('inscription-patient/', views.register_patient_view, name='register_patient'),
    path(
        'mot-de-passe-oublie/',
        views.EhsPasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'mot-de-passe-oublie/envoye/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reinitialiser/termine/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    path(
        'reinitialiser/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url=reverse_lazy('accounts:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path('tableau-de-bord/', views.dashboard_view, name='dashboard'),
]
