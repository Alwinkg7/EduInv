from datetime import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from EduInvApp.models import contactdb, clientsignupdb, investorsignupdb, loanapplicationdb, investorapplicationdb
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
import random
import string

# Create your views here.


def Adminpanelpage(request):
    return render(request, 'AdminPanel.html')

def Adminloginpage(request):
    return render(request, 'AdminLogin.html')

def clientspage(request):
    return render(request, 'Clients.html')

def investorspage(request):
    return render(request, 'Investors.html')

def contactspage(request):
    return render(request, 'Contacts.html')

def investordetailspage(request):
    return render(request, 'Investor_Details.html')

def loanapplicationspage(request):
    return render(request, 'Client_Details.html')

def Adminlogin(request):
    if request.method == "POST":
        username_r = request.POST.get('name')
        password_r = request.POST.get('password')
        if User.objects.filter(username__contains=username_r).exists():
            user = authenticate(username=username_r, password=password_r)
            if user is not None:
                login(request, user)
                request.session['name'] = username_r
                request.session['password'] = password_r
                return redirect('Adminpanelpage')
            else:
                return redirect('Adminloginpage')
        else:
            return redirect('Adminloginpage')

# Display Contact
def displaycontact(request):
    contacts = contactdb.objects.all()
    return render(request, "Contacts.html", {'contactsdata': contacts})



# Display Client Sign ups

def displayclientsignup(request):
    clients = clientsignupdb.objects.all()
    return render(request, "Clients.html", {'clientsdata': clients})

# Display Investor Sign ups
def displayinvestorsignup(request):
    investors = investorsignupdb.objects.all()
    return render(request, "Investors.html", {'investorsdata': investors})


# Display Investor details
def displayinvestordetails(request):
    investor_details = investorapplicationdb.objects.all()
    return render(request, "Investor_Details.html", {'investordetailsdata': investor_details})

# Display Applicant details
def displayloanapplications(request):
    loanapplications = loanapplicationdb.objects.all()
    return render(request, "Client_Details.html", {'loanapplicationsdata': loanapplications})

def applicantdetails(request, applicant_id):
    applicant = get_object_or_404(loanapplicationdb, id=applicant_id)
    return render(request, 'approve_applicant.html', {'applicant': applicant})

def investordetails(request, investor_id):
    investor = get_object_or_404(investorapplicationdb, id=investor_id)
    return render(request, 'approve_investor.html', {'investor': investor})

def deleteloandata(request,dataid):
    data = loanapplicationdb.objects.filter(id=dataid)
    data.delete()
    return redirect('displayloanapplications')

def deleteinvestdata(request,dataid):
    data = investorapplicationdb.objects.filter(id=dataid)
    data.delete()
    return redirect('displayinvestordetails')

def deleteclientdata(request,dataid):
    data = clientsignupdb.objects.filter(id=dataid)
    data.delete()
    return redirect('displayclientsignup')

def deleteinvestordata(request,dataid):
    data = investorsignupdb.objects.filter(id=dataid)
    data.delete()
    return redirect('displayinvestorsignup')

# Approval
def generate_otp(length=6):
    """Generate a random OTP."""
    return ''.join(random.choices(string.digits, k=length))


def approve_applicant(request, applicant_id):
    # Fetch the applicant from the database
    applicant = get_object_or_404(loanapplicationdb, id=applicant_id)

    # Debug: Check if the method is POST
    if request.method != 'POST':
        return HttpResponse("Invalid request - Only POST method is allowed.")

    # Approve the applicant and generate OTP
    try:
        applicant.is_approved = True
        otp = generate_otp()  # Ensure this function is defined elsewhere
        applicant.otp = otp
        applicant.save()

        # Generate the link to the applicant sign-in page
        sign_in_link = request.build_absolute_uri(reverse('applicant_login'))

        # Email content for approval
        subject = 'Application Approved'
        message = (f'Congratulations! Your application has been approved.\n\n'
                   f'Use the following OTP to sign in and view your offers: {otp}\n\n'
                   f'Click the link to sign in: {sign_in_link}')
        recipient = applicant.Applicant_email  # Ensure field name matches your model

        # Send the approval email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        return HttpResponse("Approval email sent successfully.")

    except Exception as e:
        # Debug: Print the exception to the server log for troubleshooting
        print(f"Error in approve_applicant: {e}")
        return HttpResponse(f"An error occurred: {e}")

def reject_applicant(request, applicant_id):
    applicant = get_object_or_404(loanapplicationdb, id=applicant_id)

    if request.method == 'POST':
        # Email content for rejection
        subject = 'Application Rejected'
        message = 'Unfortunately, your application has been rejected.'
        recipient = applicant.Applicant_email

        # Send rejection email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        return HttpResponse("Rejection email sent successfully.")

    return HttpResponse("Invalid request")


def approve_investor(request, investor_id):
    # Fetch the investor application using the provided ID
    investor = get_object_or_404(investorapplicationdb, id=investor_id)

    if request.method != 'POST':
        return HttpResponse("Invalid request - Only POST method is allowed.")

    try:
        # Approve the investor and generate OTP
        investor.is_approved = True
        otp = generate_otp()  # Ensure this function is defined elsewhere
        investor.otp = otp
        investor.save()

        # Generate the link to the investor login page
        sign_in_link = request.build_absolute_uri(reverse('investor_login'))

        # Email content for investor approval
        subject = 'Investor Application Approved'
        message = (
            f'Congratulations! Your investor application has been approved.\n\n'
            f'Use the following OTP to sign in and start investing: {otp}\n\n'
            f'Click the link to sign in: {sign_in_link}'
        )
        recipient = investor.Investor_email  # Ensure the field name matches your model

        # Send the approval email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        return HttpResponse("Approval email sent successfully.")

    except Exception as e:
        # Debug: Log the error for troubleshooting
        print(f"Error in approve_investor: {e}")
        return HttpResponse(f"An error occurred: {e}")


