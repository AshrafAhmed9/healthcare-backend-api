# Handles every doctor request: list, view one, create, edit, delete.
# Simpler than patients - there's no ownership filter, since doctors are shared.

from rest_framework import permissions, viewsets

from doctors.models import Doctor
from doctors.serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    """CRUD for doctors. Visible to any authenticated user."""

    queryset = Doctor.objects.all()  # every doctor, not filtered by who's logged in
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
