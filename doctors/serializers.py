# Converts a Doctor row into JSON and back, plus a basic sanity check.

from rest_framework import serializers

from doctors.models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "email",
            "phone",
            "years_of_experience",
            "is_available",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_years_of_experience(self, value: int) -> int:
        # Blocks obviously fake/typo'd numbers, e.g. "700 years of experience".
        if value > 70:
            raise serializers.ValidationError("Years of experience must be realistic (<= 70).")
        return value
