from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
import rest_framework.status as status
from .serializers import BookAppointmentSerializer, patientProfileSerializer, AppointmentHistorySerializer,UpdateProfilePatientSerializer, UpdateAppointmentSerializer, DoctorDetails, PatientSerializer
from .models import patient, Appointment
from .filters import DoctorFilter, AppointmentFilter
from doctor.models import doctor


class PatientProfileViewSet(ModelViewSet):

    """
    List and update a model instance.
    """

    def get_queryset(self):
        queryset = patient.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateProfilePatientSerializer
        return patientProfileSerializer

class Util:
    """
    Sending the email For new Appointment
    """
    @staticmethod
    def sent_email(data, email):
        send_mail(data['email_subject'], data['email_body'], 'mosh@mosh.com', [email])

class AppointmentViewSet(ModelViewSet):

    """
    CRUD on Appointment
    """

    http_method_names = ['get','patch','delete','post']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = AppointmentFilter
    search_field = ['service']

    def get_queryset(self):
        appointment_queryset = Appointment.objects.filter(patient_id=self.kwargs['patient_pk'])
        return appointment_queryset


    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookAppointmentSerializer
        if self.request.method == "PATCH":
            return UpdateAppointmentSerializer
        return AppointmentHistorySerializer
        
    def get_serializer_context(self):
        return {'patient_id':self.kwargs['patient_pk']}

    def create(self, request, *args, **kwargs):
        serializer = BookAppointmentSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        patient_detail = patient.objects.get(pk=self.kwargs['patient_pk'])
        doctor_active = doctor.objects.filter(zipcode=patient_detail.zipcode,service=request.data.get('service'))
        available_doctor = None
        data = request.data
        schedule_start_dummy = datetime.strptime(data.get('schedule_start'),"%Y-%m-%dt%H:%M:%S")
        schedule_end_dummy = datetime.strptime(data.get('schedule_start'),"%Y-%m-%dt%H:%M:%S")
        for d in doctor_active:

            slot_check = False
            doc_meet = Appointment.objects.filter(doctor=d)

            for appoint in doc_meet:
                
                if(d.toTime < schedule_start_dummy.time() and  d.fromTime > schedule_end_dummy.time()) and (datetime.strftime(appoint.schedule_end,"%Y-%m-%dt%H:%M:%S") < data.get('schedule_start') or datetime.strftime(appoint.schedule_start,"%Y-%m-%dt%H:%M:%S") > data.get('schedule_end')):
                    print(79,"if")
                    slot_check = True
                    continue
                else:
                    return Response({"No Slot Avaliable Please Come Back again"},status=status.HTTP_404_NOT_FOUND)
            if slot_check:
                available_doctor = doctor.objects.get(pk=d.id)
        if available_doctor is not None:
            appoint = Appointment.objects.create(
                    patient_id=self.kwargs['patient_pk'],
                    schedule_start=data.get('schedule_start'),
                    schedule_end=data.get('schedule_end'),doctor=available_doctor, service=data.get('service'),status=True)
            appoint.save()
            email_doctor = available_doctor.user.email
            email_patient = patient_detail.user.email

            schedule_start_dummy = datetime.strptime(data.get('schedule_start'),"%Y-%m-%dt%H:%M:%S")

            email_body = ' Hii {} '.format(
                available_doctor.user.first_name) + 'The New Patient {0} With having  booking slot \n date {1} start_time {2} end _time {3}  \n Please be Available' .format(patient_detail.user.first_name,schedule_start_dummy.date(),schedule_start_dummy.time(),schedule_end_dummy.time())
            data_doctor = {
                'email_body': email_body,
                'email_subject': 'Appointment Detail'
            }
            email_body_patient = 'Thank You For Choosing our Service \n \n Hii {} '.format(
                patient_detail.user.first_name) + 'We success Fully booked your slot With {0} and having slot \n date {1} time {2}'.format(available_doctor.user.first_name,schedule_start_dummy.date(),schedule_start_dummy.time())
            data_patient = {
                'email_body': email_body_patient,
                'email_subject': 'Appointment Successfull'
            }
            Util.sent_email(data_doctor,email_doctor)
            Util.sent_email(data_patient,email_patient)

            return Response(serializer.data,status=201)
        else:
            return Response({"No doctor Avaliable"},status=status.HTTP_404_NOT_FOUND)

class SearchViewSetDoctor(ModelViewSet):

    """
    Seraching the Doctor With provided condition
    """

    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = DoctorFilter
    search_field = ['service']
    queryset = doctor.objects.all()
    serializer_class = DoctorDetails


from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
class PatientViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):

    """
    Creating, Updating, Retreving the User as Patient Instance
    """

    patient = patient.objects.all()
    

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    serializer_class = PatientSerializer


    # def list(self, request, *args, **kwargs):
    #     obj = self.filter_queryset(self.get_queryset()).values_list('doctor', flat=True)
    #     doc = doctor.objects.filter(id__in=obj).values_list('user__first_name')
    #     return Response(doc)