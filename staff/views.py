from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from accounts.decorators import role_required
from accounts.forms import StaffUserForm

User = get_user_model()


@role_required(User.Role.DOCTOR)
def staff_list(request):
    staff_users = User.objects.filter(
        role__in=(User.Role.DOCTOR, User.Role.NURSE),
    ).order_by('role', 'username')
    return render(request, 'staff/staff_list.html', {'staff_users': staff_users})


@role_required(User.Role.DOCTOR)
@require_http_methods(['GET', 'POST'])
def staff_create(request):
    if request.method == 'POST':
        form = StaffUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membre du personnel créé.')
            return redirect('staff:list')
    else:
        form = StaffUserForm(initial={'role': User.Role.NURSE})
    return render(request, 'staff/staff_form.html', {'form': form, 'title': 'Nouveau membre'})


@role_required(User.Role.DOCTOR)
@require_http_methods(['GET', 'POST'])
def staff_edit(request, pk):
    user = get_object_or_404(
        User.objects.filter(role__in=(User.Role.DOCTOR, User.Role.NURSE)),
        pk=pk,
    )
    if request.method == 'POST':
        form = StaffUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour.')
            return redirect('staff:list')
    else:
        form = StaffUserForm(instance=user)
    return render(
        request,
        'staff/staff_form.html',
        {'form': form, 'title': f'Modifier {user.get_username()}'},
    )


@role_required(User.Role.DOCTOR)
@require_http_methods(['GET', 'POST'])
def staff_delete(request, pk):
    user = get_object_or_404(
        User.objects.filter(role__in=(User.Role.DOCTOR, User.Role.NURSE)),
        pk=pk,
    )
    if user.pk == request.user.pk:
        messages.error(request, 'Vous ne pouvez pas supprimer votre propre compte.')
        return redirect('staff:list')
    if request.method == 'POST':
        try:
            user.delete()
        except ProtectedError:
            messages.error(
                request,
                'Suppression impossible : des patients sont encore associés à ce compte.',
            )
            return redirect('staff:list')
        messages.success(request, 'Compte supprimé.')
        return redirect('staff:list')
    return render(request, 'staff/staff_confirm_delete.html', {'staff_user': user})
