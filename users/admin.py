from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.user import User, UserProfile

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'name', 'rol', 'is_active', 'is_staff', 'team')
    list_filter = ('rol', 'is_active', 'is_staff', 'team')
    search_fields = ('email', 'name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('name', 'team', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'rol', 'team', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_url')