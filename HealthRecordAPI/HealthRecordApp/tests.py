# HealthRecordApp/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Department, Patient, Doctor, PatientRecord

User = get_user_model()


class APITest(APITestCase):
    def setUp(self):
        # Create a department
        self.department = Department.objects.create(
            name='Cardiology',
            diagnostics='Cardiac diagnostics',
            location='New York',
            specialization='Heart'
        )

        # Create a doctor
        self.doctor_user = User.objects.create_user(
            username='doctor1', password='testpassword')
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            department=self.department
        )

        # Create a patient
        self.patient_user = User.objects.create_user(
            username='patient1', password='testpassword')
        self.patient = Patient.objects.create(
            user=self.patient_user,
            department=self.department
        )

        # Create a patient record
        self.patient_record = PatientRecord.objects.create(
            patient=self.patient,
            diagnostics='Test diagnostics',
            observations='Test observations',
            treatments='Test treatments',
            department=self.department,
            misc='Test misc'
        )

    def test_doctor_list(self):
        url = reverse('doctor-list')
        self.client.force_login(self.doctor_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], 'doctor1')

    # Rest of the test methods...
