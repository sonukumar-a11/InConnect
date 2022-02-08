from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
import rest_framework.status as status
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet, ViewSet
from .serializers import PatientRegisterSerializer, patientProfileSerializer, AppointmentHistorySerializer, \
    AppointmentSerializer, UpdateProfilePatientSerializer, UpdateAppointmentSerializer, DoctorDetails, PatientSerializer
from .models import patient, Appointment
from .filters import DoctorFilter, AppointmentFilter
from doctor.models import doctor


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
        return AppointmentHistorySerializer


class CreateAppointment(APIView):
    def __init__(self):
        super().__init__()
        self.appointment_detail = None
        self.slot = None
        self.appointment_data = None

    def get(self, request, patient_id):
        doctor_queryset = doctor.objects.all()
        doctor_detail_serializer = DoctorDetails(doctor_queryset, many=True)
        return Response(doctor_detail_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, patient_id):
        from datetime import datetime, timedelta
        patient_detail = patient.objects.filter(pk=patient_id).get()
        data = request.data
        start_datetime = datetime.strptime(data['schedule'], "%Y-%m-%dt%H:%M:%S")
        end_datetime = start_datetime + timedelta(minutes=15)
        print(62, end_datetime)
        doctor_detail = doctor.objects.filter(toTime__lte=start_datetime.time(),
                                              fromTime__gt=start_datetime.time()).filter(
            zipcode=patient_detail.zipcode).filter(
            service=data['service'])
        count = 0
        for i in doctor_detail:
            count += 1

        if count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            print("Give List")
            try:
                print(76)
                list_slot = []
                for d in doctor_detail:
                    indicate = False
                    appointment_detail = Appointment.objects.filter(doctor=d)
                    for slot in appointment_detail:
                        # ek doctor is solt me available hai
                        print(84, slot.schedule)
                        print(85, start_datetime)
                        if slot.schedule + timedelta(minutes=15) <= start_datetime:
                            print('86', 'if')
                            continue
                        # ek doctor is solt me available hai
                        elif slot.schedule > end_datetime:
                            print('90', 'elif')
                            continue
                        else:
                            indicate = True
                            print(94, indicate)
                            break
                    if indicate:
                        continue
                    else:
                        list_slot.append(doctor.object.get(id=d))
                        print(list_slot)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)


class SearchViewSetDoctor(ModelViewSet):
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = DoctorFilter
    search_field = ['service']
    queryset = doctor.objects.all()
    serializer_class = DoctorDetails


from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet


class PatientViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    patient = patient.objects.all()
    serializer_class = PatientSerializer







# {
# "service": "CL",
# "rating": 40,
# "schedule": "2011-02-06t01:00:00"
# }
