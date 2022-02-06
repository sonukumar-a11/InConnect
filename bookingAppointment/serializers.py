from rest_framework import serializers
from bookingAppointment.models import patient, Appointment
from users.models import User
from doctor.models import doctor


class PatientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']
        write_only_fields = ['password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            status=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class patientProfileSerializer(serializers.ModelSerializer):
    # email_id = serializers.EmailField(label='email')
    # city = serializers.CharField(label='City')
    # state = serializers.CharField(label='State')
    # zipcode = serializers.IntegerField(label='zipcode')

    class Meta:
        model = patient
        fields = ['email_id', 'city', 'state', 'zipcode']

    def create(self, validate_data):
        import pdb
        pdb.set_trace()
        # new_patient = patient.objects.create(
        #     email_id=validate_data['email_id'],
        #     city=validate_data['city'],
        #     state=validate_data['state'],
        #     zipcode=validate_data['zipcode'],
        #     user=validate_data['user'],
        # )
        # return new_patient
        return patient.objects.create(**validate_data)

    def update(self, instance, validate_data):
        instance.email_id = validate_data.get('email_id', instance.email_id)
        instance.city = validate_data.get('city', instance.city)
        instance.state = validate_data.get('state', instance.state)
        instance.zipcode = validate_data.get('zipcode', instance.zipcode)
        instance.save()
        return instance


class DoctorDetails(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = doctor
        fields = ['user', 'toTime', 'fromTime', 'rating', 'service']


class AppointmentSerializer(serializers.Serializer):
    doctor = DoctorDetails()

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'service', 'appointment_date', 'appointment_time']


class AppointmentHistorySerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    doctor = serializers.StringRelatedField(read_only=True)
    appointment_date = serializers.DateField(read_only=True)
    service = serializers.CharField(read_only=True)
    appointment_time = serializers.TimeField(read_only=True)

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'service', 'appointment_date', 'appointment_time', 'rating']


class UpdateProfilePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = patient
        fields = ['email_id', 'city', 'state', 'zipcode']


class UpdateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'service', 'appointment_date', 'appointment_time']
