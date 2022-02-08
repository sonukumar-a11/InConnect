from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DoctorsViewSet, DoctorViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'register', DoctorsViewSet, basename='doctor-register')
router.register(r'detail', DoctorViewSet, basename='doctor-detail')
urlpatterns = router.urls
