import uuid
from django.conf import settings
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="For identifying the doctor ")
    service = models.CharField(max_length=3, choices=service_choices, default=Cardiologist,
                               help_text="Service which is provided by doctor")
    toTime = models.TimeField(auto_now_add=False, auto_now=False, help_text="Starting time for doctor")
    fromTime = models.TimeField(auto_now_add=False, auto_now=False, help_text="Ending time for doctor")
    city = models.CharField(max_length=30, help_text="City Where doctor server your service")
    state = models.CharField(max_length=20, help_text="State City belong too")
    zipcode = models.IntegerField(help_text="City Zipcode")
    rating = models.IntegerField(validators=[check_range], help_text="Rating Your self on the basic service knowledge")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
