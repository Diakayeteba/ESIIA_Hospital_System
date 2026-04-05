from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def role_required(*roles):
    """N'autorise que les utilisateurs dont le champ `role` est dans `roles`."""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if request.user.role not in roles:
                messages.error(request, 'Accès refusé pour votre rôle.')
                return redirect('accounts:dashboard')
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
