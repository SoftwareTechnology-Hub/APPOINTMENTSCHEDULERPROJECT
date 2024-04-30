# appointments/urls.py
from django.urls import path
from .views import index, schedule_appointment, admin_confirm_appointment, admin_panel

app_name = 'appointments'

urlpatterns = [
    path('', index, name='index'),
    path('schedule/', schedule_appointment, name='schedule_appointment'),
    path('admin/confirm/<int:appointment_id>/', admin_confirm_appointment, name='admin_confirm_appointment'),
    path('admin/', admin_panel, name='admin_panel'),
]

