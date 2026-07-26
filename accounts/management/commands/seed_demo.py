from datetime import date

from django.core.management.base import BaseCommand

from accounts.models import User
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping
from patients.models import Patient


class Command(BaseCommand):
    help = "Seed the database with a demo user, doctors, patients, and mappings."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email="demo@healthcare.dev", defaults={"name": "Demo User"}
        )
        if created:
            user.set_password("DemoPass123!")
            user.save()
            self.stdout.write(
                self.style.SUCCESS("Created demo user demo@healthcare.dev / DemoPass123!")
            )

        doctors_data = [
            ("Alice Nguyen", Doctor.Specialization.CARDIOLOGY, "alice.nguyen@demo.dev", 12),
            ("Brian Okafor", Doctor.Specialization.PEDIATRICS, "brian.okafor@demo.dev", 8),
            ("Carla Ruiz", Doctor.Specialization.DERMATOLOGY, "carla.ruiz@demo.dev", 5),
        ]
        doctors = []
        for name, spec, email, years in doctors_data:
            doctor, _ = Doctor.objects.get_or_create(
                email=email,
                defaults={"name": name, "specialization": spec, "years_of_experience": years},
            )
            doctors.append(doctor)

        patients_data = [
            ("John Smith", date(1990, 4, 12), Patient.Gender.MALE),
            ("Priya Patel", date(1985, 11, 2), Patient.Gender.FEMALE),
        ]
        patients = []
        for name, dob, gender in patients_data:
            patient, _ = Patient.objects.get_or_create(
                name=name,
                created_by=user,
                defaults={"date_of_birth": dob, "gender": gender},
            )
            patients.append(patient)

        for patient, doctor in zip(patients, doctors, strict=False):
            PatientDoctorMapping.objects.get_or_create(patient=patient, doctor=doctor)

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
