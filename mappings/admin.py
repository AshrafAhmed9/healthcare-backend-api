# Makes mappings visible in Django's built-in admin site, for the developer.

from django.contrib import admin

from mappings.models import PatientDoctorMapping


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ["id", "patient", "doctor", "created_at"]
    search_fields = ["patient__name", "doctor__name"]
