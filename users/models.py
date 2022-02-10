import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STATUS_PATIENT = "PATIENT"
    STATUS_DOCTOR = "DOCTOR"
    STATUS_IDENTITY = [
        (STATUS_PATIENT, "False"),
        (STATUS_DOCTOR, "True")
    ]
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True, help_text="Using Email for Registering")
    REQUIRED_FIELDS = ['username']
    status = models.CharField(max_length=7, choices=STATUS_IDENTITY,
                              help_text="For identifying the user is Whom True -> doctor,False->Patient")

    def __str__(self):
        return str(self.first_name)
