from rest_framework import serializers

from bookingAppointment.models import Appointment
from users.models import User
from .models import doctor
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['patient', 'rating', 'appointment_date']


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctor
        field = ['id', 'service', 'toTime', 'fromTime', 'city', 'state', 'rating']


class UpdateProfileDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctor
        fields = ['service', 'toTime', 'fromTime', 'city', 'state', 'zipcode']


class DoctorSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = doctor
        fields = ['user_id', 'service', 'toTime', 'fromTime', 'city', 'state', 'zipcode', 'rating']

    def create(self, validate_data):
        user_id = self.context['user_id']
        return doctor.objects.create(user_id=user_id, **validate_data)
