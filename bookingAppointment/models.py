import uuid
from django.db import models
from django.conf import settings
from doctor.models import doctor
from django.core.validators import MinValueValidator, MaxValueValidator


class patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="To determine the unique")
    city = models.CharField(max_length=30, help_text="Patient belong to which city")
    state = models.CharField(max_length=20, help_text="Patient belong to which city")
    zipcode = models.IntegerField(help_text="City unique code ")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="For authentication")

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="To determine the unique")
    service = models.CharField(max_length=30, help_text="Use for particular service which you want")
    schedule = models.DateTimeField(help_text="for suggesting the time time as well as date")
    status = models.BooleanField(default=False, help_text="giving the status of appointment")
    patient = models.ForeignKey(patient, related_name='patient_appointments', on_delete=models.CASCADE,
                                help_text="Related field for determining the appointment for which patient ")
    doctor = models.ForeignKey(doctor, related_name='doctor_appointments', null=True, on_delete=models.SET_NULL,
                               help_text="With which doctor have booked appointment")
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=5, help_text="Give the rating for service")

    @property
    def patient_name(self):
        var = self.patient.get_name
        return var

    def __str__(self):
        return str(self.patient.user.first_name)
