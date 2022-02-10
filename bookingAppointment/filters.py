from django_filters.rest_framework import FilterSet
from bookingAppointment.models import Appointment
from doctor.models import doctor


class AppointmentFilter(FilterSet):
    class Meta:
        model = Appointment
        fields = {
            'schedule_start': ['lt', 'gt'],
            'service': ['exact'],
            'patient__zipcode': ['exact'],
            'rating': ['gte', 'lte']
        }
class DoctorFilter(FilterSet):
    class Meta:
        model = doctor
        fields = {
            'toTime': ['lt', 'gt'],
            'service': ['exact'],
            'zipcode': ['exact'],
            'rating': ['gte', 'lte']
        }
