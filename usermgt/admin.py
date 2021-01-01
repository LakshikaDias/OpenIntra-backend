from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.auth.forms import UserChangeForm
from .models import User


class UserAdmin(UserAdminBase):
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
                                    'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Work info', {
         'fields': ('role', 'department', 'extension', 'position')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ['email', 'department', 'position']
    search_fields = ['email', 'first_name',
                     'last_name', 'role', 'department', 'position']
    ordering = ('email', )


admin.site.register(User, UserAdmin)
