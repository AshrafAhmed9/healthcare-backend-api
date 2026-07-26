from django.contrib import admin

from doctors.models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "specialization", "years_of_experience", "is_available"]
    search_fields = ["name", "email"]
    list_filter = ["specialization", "is_available"]
