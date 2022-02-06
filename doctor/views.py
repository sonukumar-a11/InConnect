from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
import rest_framework.status as status
from .models import doctor
from doctor.serializers import doctorRegistrationSerializer, doctorDetailSerializer
from users.models import User


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


class DoctorViewSet(APIView):

    def get(self, request, doctor_id):
        doctor_profile = doctor.objects.filter(pk=doctor_id).get()
        user = User.objects.filter(id=doctor_profile.user_id).get()
        print(44,doctor_profile)
        print(45,user)
        user_detail = doctorRegistrationSerializer(user)
        doctor_detail = doctorDetailSerializer(doctor_profile)
        print(doctor_detail.data)
        return Response({
            'user_data': user_detail.data,
            'doctor_detail': doctor_detail.data
        }, status=status.HTTP_200_OK)

    def put(self, request, doctor_id):
        profile_doctor = \
            {
                "email_id": request.data["email_id"], "service": request.data["service"], "city": request.data["city"],
                "state": request.data["state"], "zipcode": request.data["zipcode"], "rating": request.data["rating"],
                "toTime": request.data["toTime"], "fromTime": request.data["fromTime"]
            }
        doctor_profile = doctor.objects.filter(pk=doctor_id).get()
        user = User.objects.filter(id=doctor_id)
        profileSerializer = doctorDetailSerializer(
            data=profile_doctor
        )
        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({
                'profile_data': profileSerializer.data
            })
        else:
            return Response({
                "Provided Data is not valid"
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, doctor_id):
        doctor_profile = doctor.objects.filter(pk=doctor_id).get()
        user = User.objects.filter(id=doctor_id)
        doctor_profile.delete()
        return Response({"Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

# {
#     "username":"Sonu9496",
#     "first_name":"Sonu",
#     "last_name":"Kumar",
#     "password":"Nexa9491@",
#     "password2":"Nexa9491@",
#     "email_id":"sharmasonu04359491@gmail.com",
#     "service":"CL,",
#     "city":"Noida",
#     "state":"UP",
#     "zipcode":201301,
#     "toTime": "10:30:00",
#     "fromTime":"12:30:00",
#     "rating":40
# }
