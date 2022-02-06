from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DoctorRegisterViewSet, DoctorViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'register', DoctorRegisterViewSet, basename='doctor-register')
urlpatterns = [
    path('', include(router.urls)),
    path('detail/<str:doctor_id>', DoctorViewSet.as_view(), name='api_doctor_registration'),

]
print(urlpatterns)
