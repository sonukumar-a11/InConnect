from rest_framework_nested import routers
from django.urls import path, include
from .views import PatientProfileViewSet,AppointmentViewSet, \
    SearchViewSetDoctor, PatientViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'register', PatientViewSet, basename='patient-register')
router.register(r'home', SearchViewSetDoctor, basename='search-doctor')
router.register(r'patient', PatientProfileViewSet, basename='patient_detail'),
# router.register(r'book_appointment',BookAppointmentViewSet,basename='appointment-create')
appointment_router = routers.NestedDefaultRouter(router, 'patient', lookup='patient')
appointment_router.register('appointment', AppointmentViewSet, basename='appointment')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(appointment_router.urls)),
    # path('patients/<str:patient_id>/create-appointment', CreateAppointment.as_view(), name='create_appointment'),
]
