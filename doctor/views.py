from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
import rest_framework.status as status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.decorators import action
from .models import doctor
from doctor.serializers import doctorRegistrationSerializer, doctorDetailSerializer, UpdateProfileDoctorSerializer, \
    DoctorProfileSerializer, AppointmentSerializer
from users.models import User
from bookingAppointment.models import patient, Appointment


# Create your views here.
class DoctorRegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        profile_doctor = \
            {
                "email_id": request.data["email_id"], "service": request.data["service"], "city": request.data["city"],
                "state": request.data["state"], "zipcode": request.data["zipcode"], "rating": request.data["rating"],
                "toTime": request.data["toTime"], "fromTime": request.data["fromTime"]
            }
        print(profile_doctor)
        registration_detail = doctorRegistrationSerializer(data=request.data)
        doctor_detail = doctorDetailSerializer(data=request.data)
        check_registration_detail = registration_detail.is_valid()
        check_doctor_detail = doctor_detail.is_valid()
        print(22, check_registration_detail, check_doctor_detail)
        if check_doctor_detail and check_registration_detail:
            register_doctor = registration_detail.save()
            doctor_detail.save(user=register_doctor)
            return Response(
                {
                    'user_data': registration_detail.data,
                    'detail_doctor': doctor_detail.data
                }, status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                'user_data': doctorRegistrationSerializer.errors,
                'patient_profile': doctorDetailSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics, mixins, views


class DoctorViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = UpdateProfileDoctorSerializer

    def get_queryset(self):
        queryset = doctor.objects.filter(pk=self.kwargs['pk'])
        return queryset
