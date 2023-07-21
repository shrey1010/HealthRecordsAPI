# api/urls.py
from django.urls import path
from knox import views as knox_views
from HealthRecordApp.views import (
    DepartmentListView,
    DoctorListView,
    DoctorDetailView,
    PatientListView,
    PatientDetailView,
    PatientRecordListView,
    PatientRecordDetailView,
    RegisterAPI,
    LoginAPI,
    LogoutAPI,
)

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('patient_records/', PatientRecordListView.as_view(),
         name='patient-record-list'),
    path('patient_records/<int:pk>/', PatientRecordDetailView.as_view(),
         name='patient-record-detail'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),

    # Authentication Endpoints
    path('auth/register/', RegisterAPI.as_view(), name='auth-register'),
    path('auth/login/', LoginAPI.as_view(), name='auth-login'),
    path('auth/logout/', LogoutAPI.as_view(), name='auth-logout'),
]
