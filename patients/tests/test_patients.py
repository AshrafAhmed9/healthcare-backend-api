import pytest
from rest_framework import status

from patients.models import Patient

pytestmark = pytest.mark.django_db


@pytest.fixture
def patient(user) -> Patient:
    return Patient.objects.create(
        created_by=user, name="John Doe", date_of_birth="1990-01-01", gender=Patient.Gender.MALE
    )


def test_list_requires_authentication(api_client):
    response = api_client.get("/api/patients/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_patient_sets_created_by(auth_client, user):
    response = auth_client.post(
        "/api/patients/",
        {"name": "Jane Roe", "date_of_birth": "1985-06-15", "gender": "F"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["created_by"] == user.id
    assert response.data["age"] is not None


def test_create_patient_rejects_future_dob(auth_client):
    response = auth_client.post(
        "/api/patients/",
        {"name": "Time Traveler", "date_of_birth": "2999-01-01", "gender": "M"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_only_returns_own_patients(auth_client, other_auth_client, patient):
    other_auth_client.post(
        "/api/patients/", {"name": "Bob's Patient", "date_of_birth": "1980-01-01", "gender": "M"}
    )
    response = auth_client.get("/api/patients/")
    names = [p["name"] for p in response.data["results"]]
    assert names == ["John Doe"]


def test_retrieve_own_patient(auth_client, patient):
    response = auth_client.get(f"/api/patients/{patient.id}/")
    assert response.status_code == status.HTTP_200_OK


def test_retrieve_other_users_patient_returns_404(other_auth_client, patient):
    response = other_auth_client.get(f"/api/patients/{patient.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_other_users_patient_returns_404(other_auth_client, patient):
    response = other_auth_client.put(
        f"/api/patients/{patient.id}/",
        {"name": "Hijacked", "date_of_birth": "1990-01-01", "gender": "M"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_users_patient_returns_404(other_auth_client, patient):
    response = other_auth_client.delete(f"/api/patients/{patient.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Patient.objects.filter(id=patient.id).exists()


def test_delete_own_patient(auth_client, patient):
    response = auth_client.delete(f"/api/patients/{patient.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Patient.objects.filter(id=patient.id).exists()
