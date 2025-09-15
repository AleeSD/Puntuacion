from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import EmailAuthenticationForm, UserForm
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:list')
    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, 'Bienvenido')
        return redirect('users:list')
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada')
    return redirect('users:login')


def is_admin(user):
    return user.is_authenticated and (user.rol == User.ADMIN or user.is_staff)


@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.select_related('team').all()
    return render(request, 'users/list.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def user_create(request):
    form = UserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuario creado')
        return redirect('users:list')
    return render(request, 'users/form.html', {'form': form, 'title': 'Crear usuario'})


@login_required
@user_passes_test(is_admin)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuario actualizado')
        return redirect('users:list')
    return render(request, 'users/form.html', {'form': form, 'title': 'Editar usuario'})


@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado')
        return redirect('users:list')
    return render(request, 'users/confirm_delete.html', {'object': user, 'title': 'Eliminar usuario'})

