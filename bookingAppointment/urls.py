from rest_framework_nested import routers
from django.urls import path, include
from .views import PatientProfileViewSet, CreateAppointment, AppointmentViewSet, \
    SearchViewSetDoctor, PatientViewSet

router = routers.DefaultRouter(trailing_slash=False)
# Question 1 All part
router.register(r'register', PatientViewSet, basename='patient-register')
# Part B Question 4
router.register(r'home', SearchViewSetDoctor, basename='search-doctor')
router.register(r'patient', PatientProfileViewSet, basename='patient_detail'),
appointment_router = routers.NestedDefaultRouter(router, 'patient', lookup='patient')
appointment_router.register('appointment', AppointmentViewSet, basename='appointment')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(appointment_router.urls)),
    path('patients/<str:patient_id>/create-appointment', CreateAppointment.as_view(), name='create_appointment'),
]
