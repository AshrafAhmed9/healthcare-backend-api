from django.contrib import admin

from patients.models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "gender", "date_of_birth", "created_by", "created_at"]
    search_fields = ["name", "email"]
    list_filter = ["gender"]
