from rest_framework import permissions, viewsets

from patients.models import Patient
from patients.serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """CRUD for patients. Each user only ever sees the patients they created."""

    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer: PatientSerializer) -> None:
        serializer.save(created_by=self.request.user)
