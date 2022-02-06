from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DoctorRegisterViewSet, DoctorViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'register', DoctorRegisterViewSet, basename='doctor-register')
router.register(r'detail', DoctorViewSet, basename='doctor-detail')
urlpatterns = router.urls
print(urlpatterns)
