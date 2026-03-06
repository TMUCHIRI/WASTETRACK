from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone', 'first_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('email', 'phone')
    ordering = ('email',)

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('phone', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Fields', {'fields': ('phone', 'role')}),
    )