from rest_framework_nested import routers
from django.urls import path, include
from .views import PatientProfileViewSet,AppointmentViewSet, \
    SearchViewSetDoctor, PatientViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'register', PatientViewSet, basename='patient-register')
router.register(r'home', SearchViewSetDoctor, basename='search-doctor')
router.register(r'patient', PatientProfileViewSet, basename='patient_detail'),
appointment_router = routers.NestedDefaultRouter(router, 'patient', lookup='patient')
appointment_router.register('appointment', AppointmentViewSet, basename='appointment')
urlpatterns = router.urls + appointment_router.urls