from django.db import models
from django.contrib.auth.models import Permission, User

# Create your models here.
class Appointment(models.Model):
    user = models.ForeignKey(User, default=1)
    date = models.CharField(max_length=20)
    patient_name = models.CharField(max_length=250)
    doctor = models.CharField(max_length=250)
    time = models.CharField(max_length=250)
    file_number = models.CharField(max_length=20)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.doctor + '-' + self.patient_name

class Consultation(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    consultation_number = models.CharField(max_length=250)
    doctor_name = models.CharField(max_length=250)
    patient_name = models.CharField(max_length=250)
    file_number = models.CharField(max_length=20)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.doctor_name + '-' + self.patient_name

