# Handles requests for patient-doctor mappings (list, create, look up by
# patient, delete). See the docstring on MappingDetailView below for the
# one tricky design decision in this whole project.

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mappings.models import PatientDoctorMapping
from mappings.serializers import DoctorMappingSerializer, MappingSerializer
from patients.models import Patient


class MappingListCreateView(generics.ListCreateAPIView):
    """GET: mappings for the requester's own patients. POST: assign a doctor to one."""

    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only ever return mappings for patients this user owns.
        return PatientDoctorMapping.objects.filter(patient__created_by=self.request.user)


class MappingDetailView(APIView):
    """
    The assignment description uses the same URL shape for two different
    lookups, and they don't mean the same thing:

        GET /api/mappings/<id>/    -> doctors assigned to the PATIENT with this id
        DELETE /api/mappings/<id>/ -> delete the MAPPING with this id

    A normal DRF router can only give one meaning to "<id>" for a given URL,
    so both cases are handled by hand in one view here, based on which HTTP
    method was used.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, id: int) -> Response:
        # Here "id" means a patient id - find that patient (only if it's
        # this user's own), then list every doctor assigned to them.
        patient = get_object_or_404(Patient, pk=id, created_by=request.user)
        mappings = PatientDoctorMapping.objects.filter(patient=patient)
        return Response(DoctorMappingSerializer(mappings, many=True).data)

    def delete(self, request: Request, id: int) -> Response:
        # Here "id" means a mapping id - only deletable if it belongs to
        # one of this user's own patients.
        mapping = get_object_or_404(PatientDoctorMapping, pk=id, patient__created_by=request.user)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
