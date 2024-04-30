# appointments/models.py
from django.db import models

class Appointment(models.Model):
    appointment_date = models.DateField()
    reason = models.TextField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment on {self.appointment_date}"
