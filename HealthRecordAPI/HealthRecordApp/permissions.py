# api/permissions.py
from rest_framework import permissions


def is_doctor(user):
    return hasattr(user, 'doctor')


def is_patient(user):
    return hasattr(user, 'patient')


class IsDoctorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or is_doctor(request.user)


class IsPatientOrDoctorReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (is_patient(request.user) and obj.patient.user == request.user) or (is_doctor(request.user) and obj.department == request.user.doctor.department)
