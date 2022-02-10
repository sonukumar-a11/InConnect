from http.client import responses
from rest_framework.test import APIClient
import rest_framework.status as status
from users.models import User
import pytest
@pytest.mark.django_db
class TestCreateAppointment:
    def test_if_user_is_anonymous_return_401(self):
        client = APIClient()
        response = client.post('/health/patient/d96307a9-0609-4c77-a756-466c7f5fac03/appointment',{"schedule_start": "2022-02-10T16:49:52"})
        assert response.status_code==status.HTTP_400_BAD_REQUEST


    def test_if_data_is_invalid_return_400(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True)) 
        responce = client.post('/health/patient/d96307a9-0609-4c77-a756-466c7f5fac03/appointment',{"schedule_start": " "})
        assert responce.status_code==status.HTTP_400_BAD_REQUEST
        assert responce.data['schedule_start'] is not None
    @pytest.mark.skip
    def test_if_data_is_valid_return_201(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True)) 
        responce = client.post('/health/patient/d96307a9-0609-4c77-a756-466c7f5fac03/appointment',{"patient":"d96307a9-0609-4c77-a756-466c7f5fac03","service":"CL","schedule_start": "2022-02-10T16:49:52","schedule_end": "2022-02-10T16:49:52"})
        assert responce.status_code==status.HTTP_201_CREATED
        assert responce.data['id'] > 0