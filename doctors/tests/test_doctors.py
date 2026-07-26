import pytest
from rest_framework import status

from doctors.models import Doctor

pytestmark = pytest.mark.django_db


@pytest.fixture
def doctor() -> Doctor:
    return Doctor.objects.create(
        name="Dr Smith",
        specialization=Doctor.Specialization.CARDIOLOGY,
        email="drsmith@test.com",
        years_of_experience=10,
    )


def test_list_requires_authentication(api_client):
    response = api_client.get("/api/doctors/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_doctor(auth_client):
    response = auth_client.post(
        "/api/doctors/",
        {
            "name": "Dr Jones",
            "specialization": "NEUROLOGY",
            "email": "drjones@test.com",
            "years_of_experience": 5,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_doctor_rejects_unrealistic_experience(auth_client):
    response = auth_client.post(
        "/api/doctors/",
        {
            "name": "Dr Old",
            "specialization": "GENERAL",
            "email": "drold@test.com",
            "years_of_experience": 200,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_returns_all_doctors_regardless_of_creator(auth_client, other_auth_client, doctor):
    response_a = auth_client.get("/api/doctors/")
    response_b = other_auth_client.get("/api/doctors/")
    assert response_a.data["count"] == response_b.data["count"] == 1


def test_retrieve_doctor(auth_client, doctor):
    response = auth_client.get(f"/api/doctors/{doctor.id}/")
    assert response.status_code == status.HTTP_200_OK


def test_update_doctor(auth_client, doctor):
    response = auth_client.put(
        f"/api/doctors/{doctor.id}/",
        {
            "name": "Dr Smith Jr",
            "specialization": "CARDIOLOGY",
            "email": doctor.email,
            "years_of_experience": 11,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Dr Smith Jr"


def test_delete_doctor(auth_client, doctor):
    response = auth_client.delete(f"/api/doctors/{doctor.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Doctor.objects.filter(id=doctor.id).exists()
