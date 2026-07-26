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
        return PatientDoctorMapping.objects.filter(patient__created_by=self.request.user)


class MappingDetailView(APIView):
    """
    The assignment reuses one URL shape for two different lookups:
    GET /api/mappings/<id>/    -> doctors assigned to the patient with this id
    DELETE /api/mappings/<id>/ -> remove the mapping with this id

    Both are implemented here, dispatching on HTTP method, since a single
    DRF router route can't express two different id meanings for one path.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, id: int) -> Response:
        patient = get_object_or_404(Patient, pk=id, created_by=request.user)
        mappings = PatientDoctorMapping.objects.filter(patient=patient)
        return Response(DoctorMappingSerializer(mappings, many=True).data)

    def delete(self, request: Request, id: int) -> Response:
        mapping = get_object_or_404(PatientDoctorMapping, pk=id, patient__created_by=request.user)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
