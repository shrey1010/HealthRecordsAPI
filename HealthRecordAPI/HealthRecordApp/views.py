from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from .models import Department, Patient, Doctor, PatientRecord
from .serializers import DepartmentSerializer, PatientSerializer, DoctorSerializer, PatientRecordSerializer, CustomUserSerializer
from .permissions import IsDoctorOrReadOnly, IsPatientOrDoctorReadOnly


def is_doctor(user):
    return hasattr(user, 'doctor')


def is_patient(user):
    return hasattr(user, 'patient')


class DepartmentListView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]


class DoctorListView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        if is_doctor(self.request.user):
            return Doctor.objects.filter(user=self.request.user)
        return Doctor.objects.none()


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if is_doctor(self.request.user):
            return Doctor.objects.get(user=self.request.user)
        return None


class PatientListView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrReadOnly]

    def get_queryset(self):
        if is_doctor(self.request.user):
            return Patient.objects.filter(doctor__user=self.request.user)
        return Patient.objects.none()


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsPatientOrDoctorReadOnly]

    def get_object(self):
        if is_patient(self.request.user):
            return Patient.objects.get(user=self.request.user)
        elif is_doctor(self.request.user):
            try:
                patient = Patient.objects.get(
                    user__doctor__user=self.request.user)
                if patient.user.doctor.department == self.get_object().user.doctor.department:
                    return patient
            except Patient.DoesNotExist:
                pass
        return None


class PatientRecordListView(generics.ListCreateAPIView):
    queryset = PatientRecord.objects.all()
    serializer_class = PatientRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if is_doctor(self.request.user):
            return PatientRecord.objects.filter(department=self.request.user.doctor.department)
        return PatientRecord.objects.none()


class PatientRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientRecord.objects.all()
    serializer_class = PatientRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            record = PatientRecord.objects.get(pk=self.kwargs['pk'])
            if is_patient(self.request.user) and record.patient.user == self.request.user:
                return record
            elif is_doctor(self.request.user) and record.department == self.request.user.doctor.department:
                return record
        except PatientRecord.DoesNotExist:
            pass
        return None

# Remaining views for Department Doctors and Patients not shown for brevity


class RegisterAPI(generics.GenericAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)


class LogoutAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        request._auth.delete()
        return Response("Successfully logged out", status=204)
