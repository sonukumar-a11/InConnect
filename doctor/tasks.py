import datetime
from encodings import utf_8
from celery import shared_task
from __future__ import unicode_

from bookingAppointment.models import Appointment
from doctor.models import doctor
@shared_task
def report_genertaor_on_rating():
    """
        Celery Task Genration on tteh basis of rating
    """
    with open('doctor/sortonrating.txt','w',encoding=utf_8-8) as f:
        f.write('\nUpdated Ratings List at: '+str(datetime.now()))
        f.write('\n')
        average_ratings_dict = {}
    doctors_id = doctor.objects.all().values_list('id')
    for i in doctors_id:
        doctors_name = doctor.objects.filter(id=i).values_list('name',
                                                                flat=True)
        assigned_doctor = Appointment.objects.filter(assigned_doctor=i).values_list(
                                                                    'rating',
                                                                    flat=True)
        meets = []
        for element in assigned_doctor:
            meets.append(int(element))
        if len(meets) == 0:
            doctor_rating = 0
        else:
            doctor_rating = sum(meets)/len(meets)
        average_ratings_dict[doctors_name[0]] = doctor_rating

    sorted_ratings = sorted(average_ratings_dict.items(), key=lambda x: x[1])
    for line in sorted_ratings:
        with open("doctor/sortonrating.txt", 'a', encoding='utf-8') as report_file:
            report_file.write(str(line))
            report_file.write('\n')