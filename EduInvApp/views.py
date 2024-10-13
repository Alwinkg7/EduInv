
from django.shortcuts import render, redirect, get_object_or_404
from EduInvApp.models import clientsignupdb, investorsignupdb, contactdb, investorapplicationdb, loanapplicationdb, InvestorOffer
from django.http import HttpResponse, request
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import stripe
from .models import LoanRepayment
from .forms import InstallmentPaymentForm
# from EduInvApp.forms import OfferForm
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.urls import reverse
from EduInvApp.models import Offer, loanapplicationdb
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import loanapplicationdb, Offer  # Adjust import according to your models
# Create your views here.
# Webpages
def homepage(request):
    return render(request, "home.html")

def aboutpage(request):
    return render(request, "about.html")

def contactpage(request):
    return render(request, "contact.html")

def clientsignuppage(request):
    return render(request, "ClientSignInSignUp.html")

def investorsignuppage(request):

    return render(request, "InvestorSignInSignUp.html")


# EduinvApp/views.py

# clientpage function - used for rendering a basic client page
def clientpage(request):
    if request.method == "POST":
        # Instead of handling form processing directly here, delegate to saveapplicantloan
        return saveapplicantloan(request)

    # For GET request, render the loan application form
    return render(request, 'Client.html')

# client_dashboard function - used for rendering the client dashboard with specific details
def client_dashboard(request):
    client_id = request.session.get('client_id')  # Get client ID from session
    if not client_id:
        return redirect('clientsignuppage')  # If client not logged in, redirect to signup page

    # Fetch the client (using your existing client model)
    client = get_object_or_404(clientsignupdb, id=client_id)

    # Fetch offers related to the client
    offers = Offer.objects.filter(applicant=client)

    return render(request, 'client_dashboard.html', {'client': client, 'offers': offers})

def applyforloanpage(request):
    return render(request, "ApplyForLoan.html")

def investorpage(request):
    # Fetch approved applicants
    approved_applicants = loanapplicationdb.objects.filter(is_approved=True)

    return render(request, "Investor.html", {'approved_applicants': approved_applicants})

def investnowpage(request):
    return render(request, "Investnow.html")


# database
# Client sign up

def savedatasignuppageclient(request):
    if request.method == "POST":
        # Retrieve form data
        username = request.POST.get('username')
        useremail = request.POST.get('useremail')
        userpassword = request.POST.get('userpassword')

        # Basic validation
        if not username or not useremail or not userpassword:
            messages.error(request, "All fields are required.")
            return redirect('clientsignuppage')  # Redirect back to the sign-up page

        # Check if the email already exists
        if clientsignupdb.objects.filter(clientemail=useremail).exists():
            messages.error(request, "Email is already registered.")
            return redirect('clientsignuppage')  # Redirect back to the sign-up page

        # Create and save new client record
        obj = clientsignupdb(clientname=username, clientemail=useremail, clientpassword=userpassword)
        obj.save()

        # Optionally, you can add a success message
        messages.success(request, "Registration successful! Please log in.")

        return redirect('userloginpageclient')  # Redirect to the login page after successful sign-up

    # If not POST, render the sign-up page
    return render(request, 'ClientSignInSignUp.html')

# Investor sign up

def savedatasignuppageinvestor(request):
    if request.method == "POST":
        Username = request.POST.get('username')
        Useremail = request.POST.get('useremail')
        Userpassword = request.POST.get('userpassword')
        obj = investorsignupdb(investorname=Username, investoremail=Useremail, investorpassword=Userpassword)
        obj.save()
        return redirect('investorsignuppage')

# login/signin

def userloginpageclient(request):
    if request.method == "POST":
        useremail_r = request.POST.get('useremail')
        userpassword_r = request.POST.get('userpassword')

        # Basic validation
        if not useremail_r or not userpassword_r:
            return HttpResponse("Email and password are required.")

        try:
            client = clientsignupdb.objects.get(clientemail=useremail_r, clientpassword=userpassword_r)
        except clientsignupdb.DoesNotExist:
            return HttpResponse("Invalid login credentials")

        # Save client_id in session
        request.session['client_id'] = client.id

        # Redirect to the clientpage with client_id
        return redirect('clientpage')

    # If not POST, redirect to the sign-up page or login page
    return redirect('clientsignuppage')

def userloginpageinvestor(request):
    if request.method == "POST":
        username_r = request.POST.get('username')
        useremail_r = request.POST.get('useremail')
        userpassword_r = request.POST.get('userpassword')
        if investorsignupdb.objects.filter(investoremail=useremail_r, investorpassword=userpassword_r).exists():
            request.session['usernamel'] = username_r
            request.session['useremaill'] = useremail_r
            request.session['passwordl'] = userpassword_r
            return redirect('investorpage')
        else:
            return redirect('investorsignuppage')
    return redirect('investorsignuppage')

# Log out/ Sign out

def userlogoutpageclient(request):
    del request.session['usernamel']
    del request.session['useremaill']
    del request.session['password']
    return redirect('homepage')

def userlogoutpageinvestor(request):
    del request.session['useremaill']
    del request.session['passwordl']
    return redirect('homepage')


# Save about
def savedatacontact(request):
    if request.method == "POST":
        Cname = request.POST.get('cname')
        Cemail = request.POST.get('cemail')
        Csubject = request.POST.get('csubject')
        Cmessage = request.POST.get('cmessage')
        obj1 = contactdb(contactname=Cname, contactemail=Cemail, contactsubject=Csubject, contactmessage=Cmessage)
        obj1.save()
        return redirect('contactpage')


# Save loan application
def saveapplicantloan(request):
    if request.method == "POST":
        applicantloanamount = request.POST.get('applicant_loan_amount')
        applicantgender = request.POST.get('applicant_gender')
        applicantfirstname = request.POST.get('applicant_first_name')
        applicantlastname = request.POST.get('applicant_last_name')
        applicantdob = request.POST.get('applicant_dob')
        applicantemail = request.POST.get('applicant_email')
        applicantphone = request.POST.get('applicant_phone_number')
        applicantfname = request.POST.get('applicant_father_name')
        applicantmname = request.POST.get('applicant_mother_name')
        applicantfphone = request.POST.get('applicant_father_phone')
        applicantmphone = request.POST.get('applicant_mother_phone')
        applicantfjob = request.POST.get('applicant_father_job')
        applicantmjob = request.POST.get('applicant_mother_job')
        applicantmaritalsts = request.POST.get('applicant_marital_status')
        applicanthousenumber = request.POST.get('applicant_house_number')
        applicantstreetname = request.POST.get('applicant_street_name')
        applicantpostoffice = request.POST.get('applicant_post_office')
        applicantcity = request.POST.get('applicant_city')
        applicantstate = request.POST.get('applicant_state')
        applicantcountry = request.POST.get('applicant_country')
        applicantpincode = request.POST.get('applicant_pincode')
        applicanthighestqualification = request.POST.get('applicant_highest_qualification')
        applicantmarkshighestqualification = request.POST.get('applicant_marks_highest_qualification')
        applicantmarkshse = request.POST.get('applicant_marks_hse')
        applicantmarkssslc = request.POST.get('applicant_marks_sslc')

        # Co-applicant details
        coapplicantgender = request.POST.get('co-applicant_gender')
        coapplicantfirstname = request.POST.get('co-applicant_first_name')
        coapplicantlastname = request.POST.get('co-applicant_last_name')
        coapplicantemail = request.POST.get('co-applicant_email')
        coapplicantphone = request.POST.get('co-applicant_phone_number')
        coapplicantrelation = request.POST.get('co-applicant_relation')
        coapplicantjob = request.POST.get('co-applicant_job')
        coapplicantaddress = request.POST.get('co-applicant_address')

        # College details
        applicantcollegename = request.POST.get('applicant_college_name')
        applicantuniversity = request.POST.get('applicant_university')
        applicantcollegelocation = request.POST.get('applicant_college_location')

        # Bank Details
        applicantaccountnumber = request.POST.get('applicant_account_number')
        applicantifsccode = request.POST.get('applicant_ifsc_code')
        applicantbankname = request.POST.get('applicant_bank_name')
        applicantbankbranch = request.POST.get('applicant_bank_branch_name')

        # File fields
        applicantphoto = request.FILES.get('applicant_photo')
        applicantaadhaar = request.FILES.get('applicant_aadhaar')
        applicantincomecertifiate = request.FILES.get('applicant_income_certificate')
        applicantpancard = request.FILES.get('applicant_pancard')
        applicantrationcard = request.FILES.get('applicant_ration_card')
        applicantbankpassbook = request.FILES.get('applicant_bank_passbook')
        applicantanyid = request.FILES.get('applicant_any_id')
        applicantbirthcertificate = request.FILES.get('applicant_birth_certificate')
        applicantsslccertificate = request.FILES.get('applicant_sslc_certificate')
        applicantpluscertificate = request.FILES.get('applicant_plus2_certificate')
        applicanthighestqualificationcertificate = request.FILES.get('applicant_highest_qualification_certificate')

        coapplicantphoto = request.FILES.get('co-applicant_photo')
        coapplicantaadhaar = request.FILES.get('co-applicant_aadhaar')
        coapplicantpancard = request.FILES.get('co-applicant_pancard')
        coapplicantpassbook = request.FILES.get('co-applicant_bank_passbook')
        coapplicantanyid = request.FILES.get('co-applicant_any_id')

        applicantbonafidecertifate = request.FILES.get('applicant_bonafide_certificate')
        applicantfeestructure = request.FILES.get('applicant_fee_structure')
        applicantdemandletter = request.FILES.get('applicant_demand_letter')
        applicantentrancescorecard = request.FILES.get('applicant_entrance_scorecard')
        applicantloanapproval = request.FILES.get('applicant_loan_approval')

        # Save to database
        obj = loanapplicationdb(
            Applicant_loan_amount=applicantloanamount,
            Applicant_gender=applicantgender,
            Applicant_first_name=applicantfirstname,
            Applicant_last_name=applicantlastname,
            Applicant_dob=applicantdob,
            Applicant_email=applicantemail,
            Applicant_phone_number=applicantphone,
            Applicant_father_name=applicantfname,
            Applicant_mother_name=applicantmname,
            Applicant_father_phone=applicantfphone,
            Applicant_mother_phone=applicantmphone,
            Applicant_father_job=applicantfjob,
            Applicant_mother_job=applicantmjob,
            Applicant_marital_status=applicantmaritalsts,
            Applicant_house_number=applicanthousenumber,
            Applicant_street_name=applicantstreetname,
            Applicant_post_office=applicantpostoffice,
            Applicant_city=applicantcity,
            Applicant_state=applicantstate,
            Applicant_country=applicantcountry,
            Applicant_pincode=applicantpincode,
            Applicant_highest_qualification=applicanthighestqualification,
            Applicant_marks_highest_qualification=applicantmarkshighestqualification,
            Applicant_marks_hse=applicantmarkshse,
            Applicant_marks_sslc=applicantmarkssslc,
            Co_applicant_gender=coapplicantgender,
            Co_applicant_first_name=coapplicantfirstname,
            Co_applicant_last_name=coapplicantlastname,
            Co_applicant_email=coapplicantemail,
            Co_applicant_phone_number=coapplicantphone,
            co_applicant_relation=coapplicantrelation,
            co_applicant_job=coapplicantjob,
            co_applicant_address=coapplicantaddress,
            Applicant_college_name=applicantcollegename,
            Applicant_university=applicantuniversity,
            Applicant_college_location=applicantcollegelocation,
            Applicant_account_number=applicantaccountnumber,
            Applicant_ifsc_code=applicantifsccode,
            Appicant_bank_name=applicantbankname,
            Applicant_bank_branch=applicantbankbranch,
            Applicant_photo=applicantphoto,
            Applicant_aadhaar=applicantaadhaar,
            Applicant_income_certificate=applicantincomecertifiate,
            Applicant_pancard=applicantpancard,
            Applicant_ration_card=applicantrationcard,
            Applicant_bank_passbook=applicantbankpassbook,
            Applicant_any_id=applicantanyid,
            Applicant_birth_certificate=applicantbirthcertificate,
            Applicant_sslc_certificate=applicantsslccertificate,
            Applicant_plus2_certificate=applicantpluscertificate,
            Applicant_highest_qualification_certificate=applicanthighestqualificationcertificate,
            Co_applicant_photo=coapplicantphoto,
            Co_applicant_aadhaar=coapplicantaadhaar,
            Co_applicant_pancard=coapplicantpancard,
            Co_applicant_bank_passbook=coapplicantpassbook,
            Co_applicant_any_id=coapplicantanyid,
            Applicant_bonafide_certificate=applicantbonafidecertifate,
            Applicant_fee_structure=applicantfeestructure,
            Applicant_demand_letter=applicantdemandletter,
            Applicant_entrance_scorecard=applicantentrancescorecard,
            Applicant_loan_approval=applicantloanapproval
        )
        obj.save()
        return redirect('applyforloanpage')
    else:
        return HttpResponse("Invalid request")


# Save investor application

def saveinvestorapplication(request):
    if request.method == "POST":
        Investorfirstname = request.POST.get('investor_first_name')
        Investorlastname = request.POST.get('investor_last_name')
        Investoremail = request.POST.get('investor_email')
        Nomineefirstname = request.POST.get('nominee_first_name')
        Nomineelastname = request.POST.get('nominee_last_name')
        Investoraddress = request.POST.get('investor_address')
        Investorphone = request.POST.get('investor_phone')
        Nomineephone = request.POST.get('nominee_phone')
        Investorphoto = request.FILES.get('investor_photo')
        Investorpan = request.FILES.get('investor_pan')
        Investoraadhaar = request.FILES.get('investor_aadhaar')
        Investorbankstatement = request.FILES.get('investor_bank_statement')
        Investorbankpass = request.FILES.get('investor_bank_pass')
        obj = investorapplicationdb(Investor_first_name=Investorfirstname, Investor_last_name=Investorlastname, Investor_email=Investoremail, Nominee_first_name=Nomineefirstname, Nominee_last_name=Nomineelastname, Investor_adress=Investoraddress, Investor_phone=Investorphone, Nominee_phone=Nomineephone, Investor_photo=Investorphoto, Investor_pan=Investorpan, Investor_adhaar=Investoraadhaar, Investor_bank_statement=Investorbankstatement, Investor_bank_pass=Investorbankpass)
        obj.save()
        return HttpResponse("Registration successful. Awaiting admin approval.")
    return render(request, 'Investor_Details.html')


def applicant_details(request, applicant_id):
    applicant = get_object_or_404(loanapplicationdb, id=applicant_id)

    if request.method == 'POST':
        # Get form data from POST request
        offer_amount = request.POST.get('offer_amount')
        interest_rate = request.POST.get('interest_rate')
        duration = request.POST.get('duration')

        # Validate the data (simple validation example)
        if offer_amount and interest_rate and duration:
            # Create a new offer manually without using a form
            offer = InvestorOffer(
                investor=request.user,  # Assuming the user is the investor
                applicant=applicant,
                offer_amount=offer_amount,
                interest_rate=interest_rate,
                duration=duration
            )
            offer.save()

            # Send email to the applicant
            submit_offer(applicant, Offer)

            # Refresh the page to show the new offer
            return redirect('applicant_details', applicant_id=applicant_id)
        else:
            # Handle the case where data is invalid (e.g., missing fields)
            return render(request, 'applicant_details.html', {'applicant': applicant, 'error': 'All fields are required.'})

    context = {
        'applicant': applicant,
    }
    return render(request, 'applicant_details.html', context)



# views.py
def client_details(request, client_id):
    client = get_object_or_404(loanapplicationdb, id=client_id)
    offers = Offer.objects.filter(applicant=client)

    # Render client details with the offer submission form
    form = Offer()
    return render(request, 'Client.html', {
        'client': client,
        'offers': offers,
        'form': form
    })



def submit_offer(request, applicant_id):
    if request.method == 'POST':
        # Get investor details from session
        investor_id = request.session.get('investor_id')
        investor = get_object_or_404(investorapplicationdb, id=investor_id)

        # Get form data
        offer_amount = request.POST.get('offer_amount')
        interest_rate = request.POST.get('interest_rate')
        duration = request.POST.get('duration')

        # Find the applicant
        applicant = get_object_or_404(loanapplicationdb, id=applicant_id)

        # Save the offer in the database
        offer = Offer(
            investor=investor,
            applicant=applicant,
            offer_amount=offer_amount,
            interest_rate=interest_rate,
            duration=duration,
              # Initial status of the offer
        )
        offer.save()

        # Generate accept and reject URLs
        accept_url = reverse('accept_offer', args=[offer.id])
        reject_url = reverse('reject_offer', args=[offer.id])

        # Build full URLs
        accept_link = request.build_absolute_uri(accept_url)
        reject_link = request.build_absolute_uri(reject_url)

        # Generate the link to the applicant's dashboard
        dashboard_link = request.build_absolute_uri(reverse('applicant_dashboard'))

        # Email content with accept/reject buttons
        subject = 'Investment Offer from Investor'
        html_content = (
            f'<p>Dear {applicant.Applicant_first_name},</p>'
            f'<p>You have received an offer from {investor.Investor_first_name} {investor.Investor_last_name}.</p>'
            f'<ul>'
            f'<li>Amount: {offer_amount}</li>'
            f'<li>Interest Rate: {interest_rate}%</li>'
            f'<li>Duration: {duration} months</li>'
            f'</ul>'
            f'<p>You can choose to accept or reject this offer:</p>'
            f'<p>'
            f'<a href="{accept_link}" style="padding: 10px 20px; background-color: green; color: white; text-decoration: none; border-radius: 5px;">Accept Offer</a>'
            f'&nbsp;'
            f'<a href="{reject_link}" style="padding: 10px 20px; background-color: red; color: white; text-decoration: none; border-radius: 5px;">Reject Offer</a>'
            f'</p>'
            f'<p>You can also visit your <a href="{dashboard_link}">dashboard</a> to view more details.</p>'
        )

        # Send email with HTML content
        email = EmailMultiAlternatives(
            subject,
            '',  # plain text content (can be left empty if you're only using HTML)
            settings.DEFAULT_FROM_EMAIL,
            [applicant.Applicant_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        return HttpResponse("Offer submitted and email sent successfully.")

    return HttpResponse("Invalid request.")


def accept_offer(request, offer_id):
    # Get the offer using offer_id
    offer = get_object_or_404(Offer, id=offer_id)

    # Update the offer status to 'Accepted'
    offer.status = 'Accepted'
    offer.save()

    # Get the investor associated with the offer
    investor = get_object_or_404(investorapplicationdb, id=offer.investor_id)

    # Generate the payment gateway link (assumed to be handled in a function)
    payment_link = request.build_absolute_uri(reverse('payment_gateway', args=[offer.id]))

    # Send an email notification to the investor
    subject = 'Offer Accepted - Proceed to Payment'
    message = (f'Your offer to the applicant {offer.applicant} has been accepted.\n\n'
               f'Details:\nAmount: {offer.offer_amount}\nInterest Rate: {offer.interest_rate}%\n'
               f'Duration: {offer.duration} months.\n\n'
               f'Please proceed to the payment using the following link: {payment_link}')

    # Send email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [investor.Investor_email])

    return HttpResponse("Offer accepted successfully. Investor notified with payment link.")


def reject_offer(request, offer_id):
    # Get the offer using offer_id
    offer = get_object_or_404(Offer, id=offer_id)

    # Update the offer status to 'Rejected'
    offer.status = 'Rejected'
    offer.save()

    # Get the investor associated with the offer
    investor = get_object_or_404(investorapplicationdb, id=offer.investor_id)

    # Prepare and send the rejection email
    subject = 'Offer Rejected'
    message = (f'Dear {investor.Investor_first_name} {investor.Investor_last_name},\n\n'
               f'Unfortunately, your offer to the applicant {offer.applicant.Applicant_first_name} {offer.applicant.Applicant_last_name} has been rejected.\n\n'
               f'Offer Details:\n'
               f'Amount: {offer.offer_amount}\n'
               f'Interest Rate: {offer.interest_rate}%\n'
               f'Duration: {offer.duration} months.\n\n'
               f'Thank you for your interest and better luck next time.')

    # Send email to the investor
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [investor.Investor_email],
        fail_silently=False,
    )

    return HttpResponse("Offer rejected successfully. Investor notified.")

def applicant_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        # Verify the email and OTP
        applicant = loanapplicationdb.objects.filter(Applicant_email=email, otp=otp, is_approved=True).first()

        if applicant:
            # Successful login, set session variables if needed
            request.session['applicant_id'] = applicant.id
            return redirect('applicant_dashboard')  # Redirect to applicant's dashboard

        return HttpResponse("Invalid email or OTP")

    return render(request, 'applicant_login.html')


def investor_login(request):
    if request.method == 'POST':
        email = request.POST.get('useremail')
        otp = request.POST.get('otp')

        # Check if the provided email and OTP match an approved investor
        try:
            investor = get_object_or_404(investorapplicationdb, Investor_email=email, otp=otp, is_approved=True)

            # If the OTP is valid, log the investor in and redirect to the investor dashboard
            # You may need to define a session or login mechanism for the investor
            request.session['investor_id'] = investor.id  # Save investor's ID in the session
            return redirect('investor_dashboard')  # Redirect to the investor dashboard

        except investorapplicationdb.DoesNotExist:
            return HttpResponse("Invalid email or OTP")

    return render(request, 'investor_login.html')


def applicant_dashboard(request):
    applicant_id = request.session.get('applicant_id')
    if not applicant_id:
        return redirect('applicant_login')

    # Fetch the loan application details
    applicant = get_object_or_404(loanapplicationdb, id=applicant_id)

    # Fetch investor offers related to this applicant
    offers = Offer.objects.filter(applicant=applicant)

    return render(request, 'client_dashboard.html', {'applicant': applicant, 'offers': offers})


def investor_dashboard(request):
    # Check if the investor is logged in via session
    if 'investor_id' not in request.session:
        return redirect('investor_login')  # Redirect to investor login page if not logged in

    # Fetch investor ID from session
    investor_id = request.session.get('investor_id')

    # Get the investor details from the database
    investor = get_object_or_404(investorapplicationdb, id=investor_id)

    # Get the list of approved loan applicants
    applicants = loanapplicationdb.objects.filter(is_approved=True)

    # Pass both the investor name and the applicants list to the template
    context = {
        'investor_name': f"{investor.Investor_first_name} {investor.Investor_last_name}",
        'applicants': applicants
    }

    return render(request, 'investor_dashboard.html', context)


def applicant_page(request):
    applicant_id = request.session.get('applicant_id')
    if not applicant_id:
        return HttpResponse("You are not logged in.")

    application = get_object_or_404(loanapplicationdb, id=applicant_id)

    if not application.is_approved:
        return HttpResponse("You are not approved to view offers yet.")

    # Fetch offers for the applicant
    offers = Offer.objects.filter(applicant=application)

    return render(request, 'clientofferspage.html', {'offers': offers})

def send_investor_notification(offer):
    # Generate the link to the payment gateway
    payment_gateway_link = request.build_absolute_uri(reverse('payment_gateway', args=[offer.id]))

    # Email content
    subject = 'Your Offer Has Been Accepted'
    message = (f'The applicant {offer.applicant.Applicant_first_name} {offer.applicant.Applicant_last_name} has accepted your offer.\n\n'
               f'You can proceed with the payment here: {payment_gateway_link}\n')

    recipient = offer.investor.Investor_email

    # Send email to the investor
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )


stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_gateway(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)

    if request.method == 'POST':
        try:
            # Create a Stripe Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=int(offer.offer_amount * 100),  # Stripe works in cents
                currency='usd',  # Change currency if needed
                payment_method=request.POST['payment_method_id'],
                confirmation_method='manual',
                confirm=True,
            )

            # Update offer status
            offer.status = 'Funded'
            offer.save()

            # Notify the applicant and investor
            send_mail(
                'Payment Successful',
                f'The payment for your offer {offer.id} has been completed.',
                settings.DEFAULT_FROM_EMAIL,
                [offer.investor.Investor_email, offer.applicant.Applicant_email]
            )

            return HttpResponse("Payment successful!")
        except stripe.error.CardError as e:
            return HttpResponse(f"Payment failed: {e.user_message}")

    context = {
        'offer': offer,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'payment_gateway.html', context)

def process_payment(request):
    if request.method == 'POST':
        # Extract the submitted form data
        investor_name = request.POST.get('investor_name')
        amount = request.POST.get('amount')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        billing_address = request.POST.get('billing_address')

        # Process the payment logic here
        # This can either involve integrating a third-party payment gateway
        # or mock the payment for testing purposes.

        # For now, let's assume payment is successful and update the database accordingly.
        try:
            # Assuming the payment is successful, update the offer status or any other details.
            # You may want to store transaction details in a database or log them.

            # Notify the investor and applicant about the successful payment via email
            subject = 'Payment Successful'
            message = f'Thank you, {investor_name}! Your payment of {amount} has been received.'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email])  # Send to logged-in investor

            return HttpResponse("Payment successful. You will be notified via email.")
        except Exception as e:
            return HttpResponse(f"Payment failed: {e}")

    return HttpResponse("Invalid request.")


# Top Investors
def top_investors(request):
    # Aggregate total investments by each investor
    top_investors = (Offer.objects
                     .filter(status='Accepted')  # Only consider accepted offers
                     .values('investor')  # Group by investor
                     .annotate(total_investment=Sum('offer_amount'))  # Sum offer_amount for each investor
                     .order_by('-total_investment'))  # Order by total investment in descending order

    # Fetch investor details
    investors = []
    for investor_data in top_investors:
        investor = investorapplicationdb.objects.get(id=investor_data['investor'])
        investors.append({
            'name': f"{investor.Investor_first_name} {investor.Investor_last_name}",
            'email': investor.Investor_email,
            'total_investment': investor_data['total_investment']
        })

    return render(request, 'home.html', {'investors': investors})



def loan_repayment(request, loan_id):
    repayment = get_object_or_404(LoanRepayment, applicant_id=loan_id)

    if request.method == 'POST':
        form = InstallmentPaymentForm(request.POST)
        if form.is_valid():
            installment_amount = form.cleaned_data['installment_amount']

            # Check if the payment matches the installment amount (EMI)
            if installment_amount == repayment.monthly_installment:
                repayment.installments_paid += 1
                repayment.next_due_date = timezone.now() + timezone.timedelta(days=30)  # Move due date to next month
                repayment.save()

                # Check if all installments are paid
                if repayment.installments_paid >= repayment.total_installments:
                    repayment.status = 'Completed'
                    repayment.save()

                # Send confirmation email to applicant
                send_mail(
                    'Installment Payment Successful',
                    f'You have successfully paid an installment of {installment_amount}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [repayment.applicant.Applicant_email]
                )
                return redirect('repayment_success')  # Redirect to a success page
            else:
                form.add_error('installment_amount', 'The installment amount must match the required installment.')

    else:
        form = InstallmentPaymentForm(initial={'installment_amount': repayment.monthly_installment})

    return render(request, 'loan_repayment.html', {'form': form, 'repayment': repayment})

def repayment_success(request):
    return render(request, 'repayment_success.html')