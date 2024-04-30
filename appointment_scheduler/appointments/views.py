# appointments/views.py
from django.shortcuts import render, redirect
from .models import Appointment

def index(request):
    return render(request, 'appointments/index.html')

def user_panel(request):
    if request.method == 'POST':
        appointment_date = request.POST['appointment_date']
        reason = request.POST['reason']
        appointment = Appointment(appointment_date=appointment_date, reason=reason)
        appointment.save()
        return redirect('user_panel')

    return render(request, 'appointments/user_panel.html')

def admin_panel(request):
    appointments = Appointment.objects.filter(is_confirmed=False)

    if request.method == 'POST':
        appointment_id = request.POST['appointment_id']
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.is_confirmed = True
        appointment.save()

    return render(request, 'appointments/admin_panel.html', {'appointments': appointments})
