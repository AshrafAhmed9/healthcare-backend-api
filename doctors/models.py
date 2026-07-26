from django.db import models


class Doctor(models.Model):
    class Specialization(models.TextChoices):
        GENERAL = "GENERAL", "General Physician"
        CARDIOLOGY = "CARDIOLOGY", "Cardiology"
        DERMATOLOGY = "DERMATOLOGY", "Dermatology"
        NEUROLOGY = "NEUROLOGY", "Neurology"
        PEDIATRICS = "PEDIATRICS", "Pediatrics"
        ORTHOPEDICS = "ORTHOPEDICS", "Orthopedics"
        PSYCHIATRY = "PSYCHIATRY", "Psychiatry"
        OTHER = "OTHER", "Other"

    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=20, choices=Specialization.choices)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Dr. {self.name} ({self.get_specialization_display()})"
