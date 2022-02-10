from datetime import datetime
from rest_framework import serializers
from bookingAppointment.models import patient, Appointment
from users.models import User
from doctor.models import doctor
class patientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = patient
        fields = ['city', 'state', 'zipcode']


class DoctorDetails(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = doctor
        fields = ['user', 'toTime', 'fromTime', 'rating', 'service']


class BookAppointmentSerializer(serializers.ModelSerializer):
    doctor_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Appointment
        fields = ['doctor_id', 'service', 'schedule_start','schedule_end']

    
class SimpleDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctor
        fields = ['toTime','fromTime','service']

class AppointmentHistorySerializer(serializers.ModelSerializer):
    # patient = serializers.StringRelatedField(read_only=True)
    # doctor = serializers.StringRelatedField(read_only=True)
    # service = serializers.CharField(read_only=True)
    doctor = SimpleDoctorSerializer()
    class Meta:
        model = Appointment
        fields = ['id','doctor', 'service','schedule_start','schedule_end','status','rating']


class UpdateProfilePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = patient
        fields = ['city', 'state', 'zipcode']


class UpdateAppointmentSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(read_only=True)
    class Meta:
        model = Appointment
        fields = ['service', 'schedule_start', 'schedule_end','status']
        

class PatientSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = patient
        fields = ['user_id', 'city', 'state', 'zipcode']
    
    def save(self, **kwargs):
        user_id = self.context['user_id']
        self.instance = patient.objects.create(user_id=user_id,**self.validated_data)
        return self.instance

