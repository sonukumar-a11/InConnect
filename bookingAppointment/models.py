import uuid
from django.db import models
from users.models import User
from doctor.models import doctor


class patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    email_id = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    service = models.CharField(max_length=30)
    appointment_date = models.DateField(verbose_name="Appointment_date", auto_now=False, auto_now_add=False)
    appointment_time = models.TimeField(verbose_name="Appointment_time", auto_now=False, auto_now_add=False)
    status = models.BooleanField(default=False)
    patient = models.ForeignKey(patient, related_name='patient_appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(doctor, related_name='doctor_appointments', null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField()

    @property
    def patient_name(self):
        var = self.patient.get_name
        return var

    def __str__(self):
        return self.patient.get_name + '-' + self.doctor.get_name

# 13:00-15:00
# 14:30
# ->
# D1: