from rest_framework import serializers

from bookingAppointment.models import Appointment
from users.models import User
from .models import doctor


class doctorRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(label='Username:')
    first_name = serializers.CharField(label='First name:')
    last_name = serializers.CharField(label='Last name:', required=False)
    password = serializers.CharField(label='password:', style={'input_type': 'password'}, write_only=True, min_length=8,
                                     help_text="Your password must contain at least 8 characters and should not be "
                                               "entirely numeric")
    password2 = serializers.CharField(label='Confirm password:', style={'input_type': 'password'}, write_only=True)

    def validate_username(self, username):
        username_exists = User.objects.filter(username__iexact=username)
        if username_exists:
            raise serializers.ValidationError({'username': 'This username already exists'})
        return username

    def validate_password(self, password):
        if password.isdigit():
            raise serializers.ValidationError('Your password should contain letters!')
        return password

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError({'password': 'password must match'})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            status=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class doctorDetailSerializer(serializers.Serializer):
    Cardiologist = 'CL'
    Dermatologists = 'DL'
    Emergency_Medicine_Specialists = 'EMC'
    Immunologists = 'IL'
    Anesthesiologists = 'AL'
    Colon_and_Rectal_Surgeons = 'CRS'
    service = serializers.ChoiceField(choices=[(Cardiologist, 'Cardiologist'),
                                               (Dermatologists, 'Dermatologists'),
                                               (Emergency_Medicine_Specialists,
                                                'Emergency Medicine Specialists'),
                                               (Immunologists, 'Immunologists'),
                                               (Anesthesiologists, 'Anesthesiologists'),
                                               (Colon_and_Rectal_Surgeons,
                                                'Colon and Rectal Surgeons')
                                               ])
    email_id = serializers.EmailField()
    city = serializers.CharField()
    state = serializers.CharField()
    zipcode = serializers.IntegerField()
    rating = serializers.IntegerField()
    toTime = serializers.TimeField()
    fromTime = serializers.TimeField()

    def create(self, validate_data):
        new_doctor = doctor.objects.create(
            service=validate_data['service'],
            email_id=validate_data['email_id'],
            toTime=validate_data['toTime'],
            fromTime=validate_data['fromTime'],
            city=validate_data['city'],
            state=validate_data['state'],
            zipcode=validate_data['zipcode'],
            rating=validate_data['rating'],
            user=validate_data['user']
        )
        return new_doctor

    def update(self, instance, validate_data):
        instance.service = validate_data.get('service', instance.service)
        instance.email_id = validate_data.get('email_id', instance.email_id)
        instance.city = validate_data.get('city', instance.city)
        instance.state = validate_data.get('state', instance.state)
        instance.zipcode = validate_data.get('zipcode', instance.zipcode)
        instance.rating = validate_data.get('rating', instance.rating)
        instance.toTime = validate_data.get('toTime', instance.toTime)
        instance.fromTime = validate_data.get('fromTime', instance.fromTime)
        instance.save()
        return instance


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ['patient', 'rating', 'appointment_date']


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctor
        field = ['email_id', 'id', 'service', 'toTime', 'fromTime', 'city', 'state', 'rating']


class UpdateProfileDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = doctor
        fields = ['email_id', 'service', 'toTime', 'fromTime', 'city', 'state', 'zipcode']
