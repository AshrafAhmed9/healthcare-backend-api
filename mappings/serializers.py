from rest_framework import serializers

from doctors.serializers import DoctorSerializer
from mappings.models import PatientDoctorMapping
from patients.models import Patient
from patients.serializers import PatientSerializer


class MappingSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source="patient", read_only=True)
    doctor_detail = DoctorSerializer(source="doctor", read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            "id",
            "patient",
            "patient_detail",
            "doctor",
            "doctor_detail",
            "notes",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
        validators = []  # uniqueness is checked in validate() for a clearer error message

    def validate_patient(self, patient: Patient) -> Patient:
        request = self.context["request"]
        if patient.created_by_id != request.user.id:
            raise serializers.ValidationError("You can only assign doctors to your own patients.")
        return patient

    def validate(self, attrs: dict) -> dict:
        patient = attrs.get("patient")
        doctor = attrs.get("doctor")
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError("This doctor is already assigned to this patient.")
        return attrs


class DoctorMappingSerializer(serializers.ModelSerializer):
    """Doctors assigned to a specific patient, as returned by the by-patient lookup."""

    doctor_detail = DoctorSerializer(source="doctor", read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "doctor", "doctor_detail", "notes", "created_at"]
