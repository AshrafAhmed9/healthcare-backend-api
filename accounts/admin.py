# Makes the User table visible and editable in Django's built-in admin site
# (the /admin/ page), mainly useful for the developer, not end users.

from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "name", "is_staff", "created_at"]
    search_fields = ["email", "name"]
