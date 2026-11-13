from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import User, Branch

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("phone",)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    ordering = ("phone",)
    list_display = ("phone", "role", "branch", "is_staff")
    search_fields = ("phone",)

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Личные данные", {"fields": ("first_name", "last_name", "email")}),
        ("Права доступа", {
            "fields": ("role", "branch", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "password1", "password2", "role", "branch"),
        }),
    )

admin.site.register(Branch)
admin.site.register(User, CustomUserAdmin)