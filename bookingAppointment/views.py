from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
import rest_framework.status as status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet, ViewSet
from .serializers import PatientRegisterSerializer, patientProfileSerializer, AppointmentHistorySerializer, \
    AppointmentSerializer, UpdateProfilePatientSerializer, UpdateAppointmentSerializer, DoctorDetails
from .models import patient, Appointment
from .filters import DoctorFilter, AppointmentFilter
from doctor.models import doctor
from users.models import User


class PatientRegisterViewSet(ViewSet):
    serializer_class = PatientRegisterSerializer

    def create(self, request):
        profile_patient = \
            {
                "email_id": request.data["email_id"], "city": request.data["city"],
                "state": request.data["state"], "zipcode": request.data["zipcode"]
            }
        data = request.data
        print(17, request.data)
        register_userSerializer = self.serializer_class(data=data)
        register_userSerializer.is_valid(raise_exception=True)
        user = register_userSerializer.save()
        # profile_patient["user"] = user.id
        patient_profileSerializer = patientProfileSerializer(data=profile_patient)
        print(30, profile_patient)
        patient_profileSerializer.is_valid(raise_exception=True)
        # print(34, str(user))
        patient_profileSerializer.save(user=user)
        return Response({
            'user_data': register_userSerializer.data,
            'patient_profile': patientProfileSerializer.data
        }, status=status.HTTP_201_CREATED)


class PatientProfileViewSet(ModelViewSet):

    def get_queryset(self):
        queryset = patient.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateProfilePatientSerializer
        return patientProfileSerializer


class AppointmentViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = AppointmentFilter
    search_field = ['service']

    def get_queryset(self):
        appointment_queryset = Appointment.objects.filter(patient_id=self.kwargs['patient_pk'])
        return appointment_queryset

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateAppointmentSerializer
        elif self.request.method == "POST":
            return AppointmentSerializer
        return AppointmentHistorySerializer


class CreateAppointment(APIView):
    def __init__(self):
        super().__init__()
        self.appointment_detail = None
        self.slot = None
        self.appointment_data = None

    print(77)

    def get(self, request, patient_id):
        # import pdb
        # pdb.set_trace()
        doctor_queryset = doctor.objects.all()
        doctor_detail_serializer = DoctorDetails(doctor_queryset, many=True)
        return Response(doctor_detail_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, patient_id):
        patient_detail = patient.objects.filter(pk=patient_id).get()
        print(patient_detail)
        data = request.data
        print(data)
        # appointment = Appointment.objects.get(service=data['service'])
        # print(92, appointment)
        doctor_detail = doctor.objects.filter(toTime__gte=data['appointment_time']). \
            filter(fromTime__lte=data['appointment_time']).filter(zipcode=patient_detail.zipcode).filter(
            service=data['service'])
        count = 0
        for i in doctor_detail:
            count += 1
        print(100, count)

        if count == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # checkDone
        else:
            print("Give List")
            try:
                self.appointment_detail = Appointment.objects.filter(doctor=doctor_detail.id).values_list(
                    'appointment_date',
                    'appointment_time')
            except:
                self.slot = request.data['appointment_time']
            try:
                from datetime import datetime, timedelta
                self.appointment_detail = max(self.appointment_detail)
                s1 = datetime.strptime(self.appointment_detail.get('appointment_time'), "%H:%M:%S")
                s2 = datetime.strptime(self.request.data.get('appointment_time'), "%H:%M:%S")
                diff = s1 - s2
                print(diff)
                if datetime.strptime(str(diff), "%H:%M:%S") < datetime.strptime("0:15:00", "%H:%M:%S"):
                    self.request.data['appointment_date'] = self.appointment_detail.get('appointment_date') + timedelta(
                        days=1)
                else:
                    self.request.data['appointment_time'] = datetime.strptime(
                        self.appointment_detail.get('appointment_time'), "%H:%M:%S") + timedelta(minutes=15)
                appointment_serializer = AppointmentSerializer(request.data)
                appointment_serializer.is_valid(raise_exception=True)
                appointment_serializer.save()
                return Response(
                    {
                        'appointment__detail': appointment_serializer.data
                    }, status=status.HTTP_201_CREATED)

            except:
                appointment_serializer = AppointmentSerializer(request.data)
                appointment_serializer.is_valid(raise_exception=True)
                appointment_serializer.save()
                return Response(
                    {
                        'appointment__detail': appointment_serializer.data
                    }, status=status.HTTP_201_CREATED)

    # def put(self, request):
    #     try:
    #         Appointment.objects.filter(pk=self.kwargs['pk'])
    #     except Exception:
    #         content = {'Patient does not exist'}
    #         return Response(content, status=status.HTTP_404_NOT_FOUND)
    #
    #     data = request.data
    #     appointmentSerializer = AppointmentSerializer(data=data)
    #     if appointmentSerializer.is_valid():
    #         appointmentSerializer.save()
    #         return Response({
    #             "appointment_data": appointmentSerializer.data
    #         }, status=status.HTTP_201_CREATED)
    #     else:
    #         content = {"Provided Data is Feasible"}
    #         return Response(content, status=status.HTTP_400_BAD_REQUEST)


class SearchViewSetDoctor(ModelViewSet):
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = DoctorFilter
    search_field = ['service']
    queryset = doctor.objects.all()
    serializer_class = DoctorDetails

# {
# "service": "Cardiologist",
# "rating": 80,
#  "appointment_date": "2011-02-06",
# "appointment_time": "04:00:00"
# }
