from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import AppointmentForm, ConsultationForm, UserForm
from .models import Appointment, Consultation


def create_appointment(request):
    if not request.user.is_authenticated():
        return render(request, 'appointment/login.html')
    else:
        form = AppointmentForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.doctor = request.user
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'appointment': appointment,
                    'form': form,
                }
                return render(request, 'appointment/create_appointment.html', context)
            appointment.save()
            return render(request, 'appointment/detail.html', {'appointment': appointment})
        context = {
            "form": form,
        }
        return render(request, 'appointment/create_appointment.html', context)


def create_consultation(request, appointment_id):
    form = ConsultationForm(request.POST or None, request.FILES or None)
    appointment  = get_object_or_404(Appointment, pk=appointment_id)
    if form.is_valid():
        appointments_consultations = appointment.consultation_set.all()
        for c in appointments_consultations:
            if c.doctor == form.cleaned_data.get("doctor"):
                context = {
                    'appointment': appointment,
                    'form': form,
                    'error_message': 'You already added that appointment',
                }
                return render(request, 'appointment/create_consultation.html', context)
        consultation = form.save(commit=False)
        consultation.appointment = appointment
        consultation.save()
        return render(request, 'appointment/detail.html', {'appointment': appointment})
    context = {
        'appointment': appointment,
        'form': form,
    }
    return render(request, 'appointment/create_consultation.html', context)


def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    appointment.delete()
    appointment = Appointment.objects.filter(user=request.user)
    return render(request, 'appointment/index.html', {'appointment': appointment})


def delete_consultation(request, appointment_id, consultation_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    consultation = Consultation.objects.get(pk=consultation_id)
    consultation.delete()
    return render(request, 'appointment/detail.html', {'appointment': appointment})


def detail(request, appointment_id):
    if not request.user.is_authenticated():
        return render(request, 'appointment/login.html')
    else:
        user = request.user
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        return render(request, 'appointment/detail.html', {'appointment': appointment, 'user': user})


def isdoctor(request, consultation_id):
    consultation = get_object_or_404(Consultation, pk=consultation_id)
    try:
        if consultation.is_doctor:
            consultation.is_doctor = False
        else:
            consultation.is_doctor = True
        consultation.save()
    except (KeyError, Consultation.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    try:
        if appointment.is_doctor:
            appointment.is_doctor = False
        else:
            appointment.is_doctor = True
        appointment.save()
    except (KeyError, Appointment.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'appointment/login.html')
    else:
        appointments = Appointment.objects.filter(user=request.user)
        consultation_results = Consultation.objects.all()
        query = request.GET.get("q")
        if query:
            appointments = appointments.filter(
                Q(doctor__icontains=query) |
                Q(patient_name__icontains=query)
            ).distinct()
            consultation_results = consultation_results.filter(
                Q(doctor__icontains=query)
            ).distinct()
            return render(request, 'appointment/index.html', {
                'appointments': appointments,
                'consultations': consultation_results,
            })
        else:
            return render(request, 'appointment/index.html', {'appointments': appointments})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'appointment/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                appointments = Appointment.objects.filter(user=request.user)
                return render(request, 'appointment/index.html', {'appointments': appointments})
            else:
                return render(request, 'appointment/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'appointment/login.html', {'error_message': 'Invalid login'})
    return render(request, 'appointment/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                appointments = Appointment.objects.filter(user=request.user)
                return render(request, 'appointment/index.html', {'appointments': appointments})
    context = {
        "form": form,
    }
    return render(request, 'appointment/register.html', context)


def consultations(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'appointment/login.html')
    else:
        try:
            consultation_ids = []
            for appointment in Appointment.objects.filter(user=request.user):
                for consultation in appointment.consultation_set.all():
                    consultation_ids.append(consultation.pk)
            users_consultations = Consultation.objects.filter(pk__in=consultation_ids)
            if filter_by == 'doctor':
                users_consultations = users_consultations.filter(is_favorite=True)
        except Appointment.DoesNotExist:
            users_consultations = []
        return render(request, 'appointment/consultations.html', {
            'consultation_list': users_consultations,
            'filter_by': filter_by,
        })





























