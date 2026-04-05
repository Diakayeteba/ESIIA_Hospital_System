"""
URL configuration for ehs_project project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

admin.site.site_header = 'ESIIA Hospital System — Admin'
admin.site.site_title = 'ESIIA Hospital System Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='accounts:dashboard', permanent=False)),
    path('comptes/', include('accounts.urls')),
    path('securite/', include('security.urls')),
    path('personnel/', include('staff.urls')),
    path('patients/', include('patients.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
