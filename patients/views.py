# Handles every patient request: list, view one, create, edit, delete.
# ModelViewSet generates all five of those automatically from the model
# and serializer below - the two methods here are the only custom behavior.

from rest_framework import permissions, viewsets

from patients.models import Patient
from patients.serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """CRUD for patients. Each user only ever sees the patients they created."""

    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]  # must be logged in

    def get_queryset(self):
        # This is the core privacy rule: every list/view/edit/delete only ever
        # searches within the current user's own patients. A patient belonging
        # to someone else simply isn't in this set, so it looks "not found".
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer: PatientSerializer) -> None:
        # Automatically stamp new patients as belonging to whoever is logged in.
        serializer.save(created_by=self.request.user)
