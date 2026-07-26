from datetime import date

from rest_framework import serializers

from patients.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "date_of_birth",
            "age",
            "gender",
            "email",
            "phone",
            "address",
            "medical_history",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def get_age(self, obj: Patient) -> int:
        today = date.today()
        dob = obj.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    def validate_date_of_birth(self, value: date) -> date:
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value
