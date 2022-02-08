from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import doctor
from doctor.serializers import UpdateProfileDoctorSerializer, \
    DoctorProfileSerializer, AppointmentSerializer, DoctorSerializer
from rest_framework import generics, mixins, views


class DoctorViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = UpdateProfileDoctorSerializer

    def get_queryset(self):
        queryset = doctor.objects.filter(pk=self.kwargs['pk'])
        return queryset


class DoctorsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = doctor.objects.all()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    serializer_class = DoctorSerializer