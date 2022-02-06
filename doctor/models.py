import uuid

from django.db import models
from users.models import User
from django.core import exceptions
from django.utils.translation import gettext_lazy as _


def check_range(value):
    if 0 < value <= 100:
        return exceptions.ValidationError(
            _('%(value)s is not in valid Range Number', params={'value': value}
              ))
    return value

class doctor(models.Model):
    Cardiologist = 'CL'
    Dermatologists = 'DL'
    Emergency_Medicine_Specialists = 'EMC'
    Immunologists = 'IL'
    Anesthesiologists = 'AL'
    Colon_and_Rectal_Surgeons = 'CRS'
    service_choices = \
        [
            (Cardiologist, 'Cardiologist'),
            (Dermatologists, 'Dermatologists'),
            (Emergency_Medicine_Specialists, 'Emergency Medicine Specialists'),
            (Immunologists, 'Immunologists'),
            (Anesthesiologists, 'Anesthesiologists'),
            (Colon_and_Rectal_Surgeons, 'Colon and Rectal Surgeons')
        ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    service = models.CharField(max_length=3, choices=service_choices, default=Cardiologist)
    toTime = models.TimeField(auto_now_add=False, auto_now=False)
    fromTime = models.TimeField(auto_now_add=False, auto_now=False)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    email_id = models.EmailField()
    rating = models.IntegerField(validators=[check_range])
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def get_name(self):
        return self.user.name
    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.username

