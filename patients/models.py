# This file defines the Patient table: what information gets stored for each patient.

from django.conf import settings
from django.db import models


class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    # Points to the user who created this patient. This is what makes each
    # patient "belong" to one account, so the API can filter by owner.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patients"
    )
    name = models.CharField(max_length=150)
    date_of_birth = models.DateField()  # age is calculated from this, not stored separately
    gender = models.CharField(max_length=1, choices=Gender.choices)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # set once, when the row is created
    updated_at = models.DateTimeField(auto_now=True)  # refreshed every time the row is saved

    class Meta:
        ordering = ["-created_at"]  # newest patients first by default

    def __str__(self) -> str:
        return self.name
