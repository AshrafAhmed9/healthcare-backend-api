# Converts a Patient row into JSON (for responses) and JSON into a Patient row
# (for create/update requests), plus checks the incoming data makes sense.

from datetime import date

from rest_framework import serializers

from patients.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    # "age" has no matching column in the database - it's worked out fresh
    # every time from date_of_birth, so it's never out of date.
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
        # These fields show up when reading a patient, but can't be set by hand
        # when creating or editing one - the server fills them in itself.
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def get_age(self, obj: Patient) -> int:
        today = date.today()
        dob = obj.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    def validate_date_of_birth(self, value: date) -> date:
        # Blocks an obviously wrong birthdate, e.g. someone born in the future.
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value
