from rest_framework_nested import routers
from django.urls import path, include
from .views import PatientProfileViewSet, PatientRegisterViewSet, CreateAppointment, AppointmentViewSet, SearchViewSetDoctor

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'register', PatientRegisterViewSet, basename='patient-register')
router.register(r'home', SearchViewSetDoctor, basename='search-doctor')
router.register(r'patient', PatientProfileViewSet, basename='patient_detail'),
appointment_router = routers.NestedDefaultRouter(router, 'patient', lookup='patient')
appointment_router.register('appointment', AppointmentViewSet, basename='appointment')
print(router)
urlpatterns = [
    path('', include(router.urls)),
    path('', include(appointment_router.urls)),
    path('patients/<str:patient_id>/appointment', CreateAppointment.as_view(), name='create_appointment'),
]
# print(urlpatterns)
