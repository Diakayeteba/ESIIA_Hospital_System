from django.urls import path

from . import views

app_name = 'security'

urlpatterns = [
    path('verifier-otp/', views.verify_otp_view, name='verify_otp'),
]
