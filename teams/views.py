from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TeamForm
from .models import Team
from users.models import User


def is_admin(user: User):
    return user.is_authenticated and (user.rol == User.ADMIN or user.is_staff)


@login_required
@user_passes_test(is_admin)
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'teams/list.html', {'teams': teams})


@login_required
@user_passes_test(is_admin)
def team_create(request):
    form = TeamForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Equipo creado')
        return redirect('teams:list')
    return render(request, 'teams/form.html', {'form': form, 'title': 'Crear equipo'})


@login_required
@user_passes_test(is_admin)
def team_update(request, pk):
    team = get_object_or_404(Team, pk=pk)
    form = TeamForm(request.POST or None, instance=team)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Equipo actualizado')
        return redirect('teams:list')
    return render(request, 'teams/form.html', {'form': form, 'title': 'Editar equipo'})


@login_required
@user_passes_test(is_admin)
def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        team.delete()
        messages.success(request, 'Equipo eliminado')
        return redirect('teams:list')
    return render(request, 'teams/confirm_delete.html', {'object': team, 'title': 'Eliminar equipo'})

