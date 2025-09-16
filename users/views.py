from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from .models import User, UserProfile
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm
from teams.models import Team

def is_admin(user):
    return user.is_authenticated and user.rol == User.ADMIN

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido/a {user.name}')
                return redirect('dashboard')
        messages.error(request, 'Credenciales incorrectas')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def user_list(request):
    if not request.user.is_admin:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('dashboard')
    
    # Añadida paginación (25 usuarios por página)
    users_list = User.objects.all().select_related('team').order_by('name')  # Optimizado con select_related
    paginator = Paginator(users_list, 25)
    
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    return render(request, 'user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Crear perfil de usuario
                UserProfile.objects.create(user=user)
                messages.success(request, 'Usuario creado exitosamente.')
                return redirect('user_list')
            except Exception as e:
                messages.error(request, f'Error al crear usuario: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CustomUserCreationForm()
    
    teams = Team.objects.all()
    return render(request, 'user_form.html', {
        'form': form,
        'teams': teams,
        'title': 'Crear Usuario',
        'action_url': 'user_create'
    })

@login_required
@user_passes_test(is_admin)
def user_update(request, pk):
    try:
        user = get_object_or_404(User, pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('user_list')
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Usuario actualizado exitosamente.')
                return redirect('user_list')
            except Exception as e:
                messages.error(request, f'Error al actualizar usuario: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CustomUserChangeForm(instance=user)
    
    teams = Team.objects.all()
    return render(request, 'user_form.html', {
        'form': form,
        'teams': teams,
        'title': 'Editar Usuario',
        'action_url': 'user_update',
        'user_id': user.id
    })

@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    try:
        user = get_object_or_404(User, pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('user_list')
    
    # No permitir auto-eliminación
    if user == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('user_list')
    
    if request.method == 'POST':
        try:
            user.delete()
            messages.success(request, 'Usuario eliminado exitosamente.')
            return redirect('user_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar usuario: {str(e)}')
            return redirect('user_list')
    
    return render(request, 'user_confirm_delete.html', {'user': user})

@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def user_toggle_active(request, pk):
    # Verificar si es una solicitud AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            user = get_object_or_404(User, pk=pk)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

        # No permitir desactivarse a sí mismo
        if user == request.user:
            return JsonResponse({'error': 'No puedes desactivar tu propio usuario.'}, status=400)

        try:
            user.is_active = not user.is_active
            user.save()
            
            return JsonResponse({
                'success': True,
                'is_active': user.is_active,
                'message': f'Usuario {"activado" if user.is_active else "desactivado"} correctamente.'
            })
        except Exception as e:
            return JsonResponse({'error': f'Error al actualizar usuario: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método no permitido o no es una solicitud AJAX.'}, status=405)

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Usa request.FILES para archivos subidos
        image = request.FILES.get('image_url')
        if image:
            user_profile.image_url = image
            try:
                user_profile.save()
                messages.success(request, 'Perfil actualizado exitosamente.')
                return redirect('profile')
            except Exception as e:
                messages.error(request, f'Error al actualizar perfil: {str(e)}')
        else:
            messages.error(request, 'Por favor sube una imagen válida.')

    return render(request, 'profile.html', {'profile': user_profile})
