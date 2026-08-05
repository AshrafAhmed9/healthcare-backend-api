# This file defines the table that links a patient to a doctor.
# Think of each row as a sticky note: "this patient sees this doctor."

from django.db import models

from doctors.models import Doctor
from patients.models import Patient


class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="doctor_mappings")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="patient_mappings")
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            # The database itself refuses a duplicate - the same doctor can't
            # be assigned to the same patient twice, even by accident.
            models.UniqueConstraint(fields=["patient", "doctor"], name="unique_patient_doctor")
        ]

    def __str__(self) -> str:
        return f"{self.patient} -> {self.doctor}"
