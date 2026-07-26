import pytest
from rest_framework import status

from doctors.models import Doctor
from mappings.models import PatientDoctorMapping
from patients.models import Patient

pytestmark = pytest.mark.django_db


@pytest.fixture
def patient(user) -> Patient:
    return Patient.objects.create(
        created_by=user, name="John Doe", date_of_birth="1990-01-01", gender=Patient.Gender.MALE
    )


@pytest.fixture
def other_patient(other_user) -> Patient:
    return Patient.objects.create(
        created_by=other_user,
        name="Bob's Patient",
        date_of_birth="1980-01-01",
        gender=Patient.Gender.MALE,
    )


@pytest.fixture
def doctor() -> Doctor:
    return Doctor.objects.create(
        name="Dr Smith",
        specialization=Doctor.Specialization.CARDIOLOGY,
        email="drsmith@test.com",
        years_of_experience=10,
    )


def test_list_requires_authentication(api_client):
    response = api_client.get("/api/mappings/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_mapping_for_own_patient(auth_client, patient, doctor):
    response = auth_client.post("/api/mappings/", {"patient": patient.id, "doctor": doctor.id})
    assert response.status_code == status.HTTP_201_CREATED


def test_create_mapping_for_other_users_patient_is_rejected(other_auth_client, patient, doctor):
    response = other_auth_client.post(
        "/api/mappings/", {"patient": patient.id, "doctor": doctor.id}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists()


def test_duplicate_mapping_is_rejected(auth_client, patient, doctor):
    PatientDoctorMapping.objects.create(patient=patient, doctor=doctor)
    response = auth_client.post("/api/mappings/", {"patient": patient.id, "doctor": doctor.id})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_only_returns_mappings_for_own_patients(auth_client, patient, other_patient, doctor):
    PatientDoctorMapping.objects.create(patient=patient, doctor=doctor)
    PatientDoctorMapping.objects.create(patient=other_patient, doctor=doctor)
    response = auth_client.get("/api/mappings/")
    assert response.data["count"] == 1
    assert response.data["results"][0]["patient"] == patient.id


def test_get_doctors_by_patient_id(auth_client, patient, doctor):
    PatientDoctorMapping.objects.create(patient=patient, doctor=doctor)
    response = auth_client.get(f"/api/mappings/{patient.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["doctor"] == doctor.id


def test_get_doctors_for_other_users_patient_returns_404(other_auth_client, patient, doctor):
    PatientDoctorMapping.objects.create(patient=patient, doctor=doctor)
    response = other_auth_client.get(f"/api/mappings/{patient.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_mapping_by_mapping_id(auth_client, patient, doctor):
    mapping = PatientDoctorMapping.objects.create(patient=patient, doctor=doctor)
    response = auth_client.delete(f"/api/mappings/{mapping.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not PatientDoctorMapping.objects.filter(id=mapping.id).exists()


def test_delete_other_users_mapping_returns_404(other_auth_client, patient, doctor):
    mapping = PatientDoctorMapping.objects.create(patient=patient, doctor=doctor)
    response = other_auth_client.delete(f"/api/mappings/{mapping.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert PatientDoctorMapping.objects.filter(id=mapping.id).exists()
