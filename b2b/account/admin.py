"""Account app admin configurations."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User

admin.site.site_header = "B2B Feedback Admin Panel"
admin.site.index_title = "Administration"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define admin model for custom User model with no username field."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    list_display = ("email", "id", "is_staff", "is_superuser")
    readonly_fields = ("last_login", "date_joined")
    search_fields = ("email",)
    ordering = ("email",)
