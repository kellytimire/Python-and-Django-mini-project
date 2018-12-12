from django.contrib.auth.models import User
from django import forms

from .models import Appointment, Consultation


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['date', 'patient_name', 'doctor', 'time', 'file_number', 'is_doctor']


class ConsultationForm(forms.ModelForm):

    class Meta:
        model = Consultation
        fields = ['consultation_number', 'doctor_name','patient_name', 'file_number', 'is_doctor']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
