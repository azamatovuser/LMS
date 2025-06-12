from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account.models import User, UserRole

class CustomUserAdmin(UserAdmin):
    ordering = ('phone_number',)
    list_display = ('id', 'phone_number', 'role', 'is_staff', 'is_active', 'created_date')
    list_filter = ('role', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('phone_number',)
    readonly_fields = ('created_date',)
    
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Role & Status', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
        }),
        ('Important dates', {'fields': ('created_date',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'role', 'is_active'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['role'].choices = UserRole.choices
        return form

admin.site.register(User, CustomUserAdmin)
