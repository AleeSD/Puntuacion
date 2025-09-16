from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ActivityForm
from .models.activity import Activity
from users.models.user import User


def is_admin(user: User) -> bool:
    return user.is_authenticated and user.is_admin


@login_required
def activity_list(request):
    activities = (
        Activity.objects.select_related('activity_type', 'user')
        .order_by('-created_at')
    )
    return render(request, 'activities/list.html', {'activities': activities})


@login_required
@user_passes_test(is_admin)
def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad creada correctamente.')
            return redirect('activity_list')
        messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ActivityForm()
    return render(request, 'activities/form.html', {'form': form, 'title': 'Crear actividad'})


@login_required
@user_passes_test(is_admin)
def activity_update(request, pk: int):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad actualizada correctamente.')
            return redirect('activity_list')
        messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'activities/form.html', {'form': form, 'title': 'Editar actividad'})


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST", "GET"])
def activity_delete(request, pk: int):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Actividad eliminada correctamente.')
        return redirect('activity_list')
    return render(request, 'activities/confirm_delete.html', {'activity': activity})
