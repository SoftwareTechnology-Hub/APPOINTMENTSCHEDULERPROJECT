from django.shortcuts import render
from .models import Appointment
# appointmentsapp/views.py
from .forms import AppointmentForm
from .models import Appointment



def index(request):
    return render(request, 'index.html')
def user_panel(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect or perform additional actions after successful form submission
            return redirect('check_appointment')  # Replace 'success_page' with the desired URL name
    else:
        form = AppointmentForm()

    return render(request, 'user_panel.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.admin.views.decorators import staff_member_required
from .models import Appointment

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.admin.views.decorators import staff_member_required
from .models import Appointment

@staff_member_required
def admin_panel(request):
    appointments = Appointment.objects.filter(is_confirmed=False)
    return render(request, 'admin_panel.html', {'appointments': appointments})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('admin_panel')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    return redirect('index')


def user_logout(request):
    auth_logout(request)
    return redirect('index')

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Appointment
from django.conf import settings

def confirm_appointment(request, appointment_id):
    # Get the appointment object
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Confirm the appointment
    appointment.is_confirmed = True
    appointment.save()

    # Get the patient's email from the related Patient model
    recipient_email = appointment.email

    # Define email parameters
    
    from_email = settings.EMAIL_HOST_USER
    subject = 'Appointment Confirmation'  # Subject of the email
    message = f'Your appointment on {appointment.appointment_date} has been confirmed.'  # Body of the email

    try:
        # Send email
        send_mail(subject, message, from_email , [recipient_email], fail_silently=False)
        return render(request, 'conformation_letter.html', {'appointment': appointment})
    except Exception as e:
        return HttpResponse('An error occurred while sending the email: {}'.format(e))
   

def confirmnot_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.is_confirmed = False
    appointment.save()
    return render(request, 'conformation_letter.html', {'appointment': appointment})


def pending_appointments(request):
    pending_appointments = Appointment.objects.filter(is_confirmed=False)
    return render(request, 'pending_appointments.html', {'pending_appointments': pending_appointments})
# appointmentsapp/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Appointment

def conformation_letter(request, appointment_id=None, email=None):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        email = request.POST.get('email')
        return HttpResponseRedirect(reverse('conformation_letter', args=[appointment_id, email]))
    else:
        if appointment_id and email:
            appointment = get_object_or_404(Appointment, id=appointment_id)
            return render(request, 'conformation_letter.html', {'appointment': appointment, 'email': email})
        else:
            # Handle the case when appointment_id and email are not provided
            pass  # Add your logic here if needed


from .forms import CheckAppointmentForm



def check_appointment(request):
    if request.method == 'POST':
        form = CheckAppointmentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            appointments = Appointment.objects.filter(email=email)
            if appointments.exists():
                return render(request, 'appointment_status.html', {'appointments': appointments})
            else:
                error_message = "No appointment found for this email address."
                return render(request, 'check_appointment.html', {'form': form, 'error_message': error_message})
    else:
        form = CheckAppointmentForm()
    return render(request, 'check_appointment.html', {'form': form})
# views.py
# views.py
from django.http import FileResponse
from django.template.loader import render_to_string
from django.utils.encoding import smart_str

# views.py
from django.http import HttpResponse
from .models import Appointment

def download_confirmation_letter(request, appointment_id):
    # Your logic to generate and return the confirmation letter as a file
    appointment = Appointment.objects.get(id=appointment_id)
    # Generate the confirmation letter content
    confirmation_letter_content = f"Appointment Confirmation for {appointment.name} id {appointment.id} date{appointment.appointment_date} is {appointment.is_confirmed} ok\n"
    # Prepare the response with the content as a file attachment
    response = HttpResponse(confirmation_letter_content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=confirmation_letter.txt'
    return response
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Appointment
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Appointment

def enter_email(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        email = request.POST.get('email')
        return HttpResponseRedirect(reverse('conformation_letter', args=[appointment_id, email]))
    else:
        return render(request, 'enter_email.html')



# views.py
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO


from io import BytesIO
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import render
from .models import Appointment

def generate_pdf(request, appointment_id):
    # Get the appointment object
    appointment = Appointment.objects.get(id=appointment_id)

    # Create a BytesIO buffer to store the PDF file
    buffer = BytesIO()

    # Create a canvas
    c = canvas.Canvas(buffer, pagesize=letter)

    # Define the text content for the PDF dynamically based on appointment details
    text_content = f"Appointment Confirmation for {appointment.name} id {appointment.id} date {appointment.appointment_date} is {appointment.is_confirmed}\n\nTrue means confirmed,false means notconfirmed"

    # Draw the text on the canvas
    c.drawString(100, 750, text_content)

    # Save the canvas as PDF
    c.save()

    # Reset the buffer pointer
    buffer.seek(0)

    # Return the PDF file as a response
    response = FileResponse(buffer, as_attachment=True, filename='generated_pdf.pdf')
    return response

# views.py

from django.core.mail import send_mail
from django.http import HttpResponse

def send_email_to_user(request):
    # Define sender, recipient, and subject
    sender_email = 'your_email@example.com'
    recipient_email = 'recipient@example.com'
    subject = 'Subject of the email'
    message = 'Body of the email'

    try:
        # Send email
        send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse('An error occurred while sending the email: {}'.format(e))



# views.py
from django.shortcuts import render


from .forms import AdminAccountForm

def create_account(request):
    if request.method == 'POST':
        form = AdminAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel.html') 
    else:
        form = AdminAccountForm()
    return render(request, 'create_account.html', {'form': form})
# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_panel')  # Redirect to admin panel
                else:
                    # Handle non-admin user login (optional)
                    pass
            else:
                # Return an 'invalid login' error message
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid login'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
