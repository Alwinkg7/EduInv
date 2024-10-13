from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
# client user
class clientsignupdb(models.Model):
    clientname = models.CharField(max_length=100)
    clientemail = models.CharField(max_length=100)
    clientpassword = models.CharField(max_length=100)
    # Add the is_approved field
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.clientname

# investor user
class investorsignupdb(models.Model):
    investorname = models.CharField(max_length=100)
    investoremail = models.EmailField()
    investorpassword = models.CharField(max_length=100)

# Contact
class contactdb(models.Model):
    contactname = models.CharField(max_length=100)
    contactemail = models.CharField(max_length=100)
    contactsubject = models.CharField(max_length=100)
    contactmessage = models.CharField(max_length=100)

#loan Application

class loanapplicationdb(models.Model):
    # Loan details
    Applicant_loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Applicant personal details
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    Applicant_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    Applicant_first_name = models.CharField(max_length=50, default='')
    Applicant_last_name = models.CharField(max_length=50, default='')
    Applicant_dob = models.DateField(default=timezone.now)  # Set default to current date
    Applicant_email = models.EmailField(default='')
    Applicant_phone_number = models.CharField(max_length=15, default='')
    Applicant_father_name = models.CharField(max_length=50, default='')
    Applicant_mother_name = models.CharField(max_length=50, default='')
    Applicant_father_phone = models.CharField(max_length=15, default='')
    Applicant_mother_phone = models.CharField(max_length=15, default='')
    Applicant_father_job = models.CharField(max_length=50, default='')
    Applicant_mother_job = models.CharField(max_length=50, default='')

    # Marital status
    Applicant_MARITAL_STATUS_CHOICES = [
        ('married', 'Married'),
        ('unmarried', 'Unmarried'),
        ('nil', 'NIL'),
    ]
    Applicant_marital_status = models.CharField(max_length=10, choices=Applicant_MARITAL_STATUS_CHOICES, default='nil')

    # Address
    Applicant_house_number = models.CharField(max_length=10, default='')
    Applicant_street_name = models.CharField(max_length=100, default='')
    Applicant_post_office = models.CharField(max_length=50, default='')
    Applicant_city = models.CharField(max_length=50, default='')
    Applicant_state = models.CharField(max_length=50, default='')
    Applicant_country = models.CharField(max_length=50, default='')
    Applicant_pincode = models.CharField(max_length=10, default='')

    # Education
    Applicant_QUALIFICATION_CHOICES = [
        ('post_graduate', 'Post Graduate'),
        ('graduate', 'Graduate'),
        ('higher_secondary', 'Higher Secondary'),
        ('high_school', 'High School'),
    ]
    Applicant_highest_qualification = models.CharField(max_length=20, choices=Applicant_QUALIFICATION_CHOICES, default='high_school')
    Applicant_marks_highest_qualification = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    Applicant_marks_hse = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    Applicant_marks_sslc = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    # Co-applicant details
    Co_applicant_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    Co_applicant_first_name = models.CharField(max_length=50, default='')
    Co_applicant_last_name = models.CharField(max_length=50, default='')
    Co_applicant_email = models.EmailField(default='')
    Co_applicant_phone_number = models.CharField(max_length=15, default='')
    RELATION_CHOICES = [
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('sibling', 'Sibling'),
        ('relative', 'Relative'),
    ]
    co_applicant_relation = models.CharField(max_length=10, choices=RELATION_CHOICES, default='relative')
    co_applicant_job = models.CharField(max_length=50, default='')
    co_applicant_address = models.CharField(max_length=255, default='')

    # College details
    Applicant_college_name = models.CharField(max_length=100, default='')
    Applicant_university = models.CharField(max_length=100, default='')
    Applicant_college_location = models.CharField(max_length=100, default='')

    # Bank Details
    Applicant_account_number = models.CharField(max_length=100, default='')
    Applicant_ifsc_code = models.CharField(max_length=100, default='')
    Appicant_bank_name = models.CharField(max_length=100, default='')
    Applicant_bank_branch = models.CharField(max_length=100, default='')

    # Document uploads
    Applicant_photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    Applicant_aadhaar = models.FileField(upload_to='aadhaar/', blank=True, null=True)
    Applicant_income_certificate = models.FileField(upload_to='income_certificates/', blank=True, null=True)
    Applicant_pancard = models.FileField(upload_to='pancards/', blank=True, null=True)
    Applicant_ration_card = models.FileField(upload_to='ration_cards/', blank=True, null=True)
    Applicant_bank_passbook = models.FileField(upload_to='bank_passbooks/', blank=True, null=True)
    Applicant_any_id = models.FileField(upload_to='id_proofs/', blank=True, null=True)
    Applicant_birth_certificate = models.FileField(upload_to='birth_certificates/', blank=True, null=True)
    Applicant_sslc_certificate = models.FileField(upload_to='sslc_certificates/', blank=True, null=True)
    Applicant_plus2_certificate = models.FileField(upload_to='plus2_certificates/', blank=True, null=True)
    Applicant_highest_qualification_certificate = models.FileField(upload_to='qualification_certificates/', blank=True, null=True)
    Co_applicant_photo = models.ImageField(upload_to='co_photos/', blank=True, null=True)
    Co_applicant_aadhaar = models.FileField(upload_to='co_aadhaar/', blank=True, null=True)
    Co_applicant_pancard = models.FileField(upload_to='co_pancards/', blank=True, null=True)
    Co_applicant_bank_passbook = models.FileField(upload_to='co_bank_passbooks/', blank=True, null=True)
    Co_applicant_any_id = models.FileField(upload_to='co_id_proofs/', blank=True, null=True)
    Applicant_bonafide_certificate = models.FileField(upload_to='bonafide_certificates/', blank=True, null=True)
    Applicant_fee_structure = models.FileField(upload_to='fee_structures/', blank=True, null=True)
    Applicant_demand_letter = models.FileField(upload_to='demand_letters/', blank=True, null=True)
    Applicant_entrance_scorecard = models.FileField(upload_to='entrance_scorecards/', blank=True, null=True)
    Applicant_loan_approval = models.FileField(upload_to='loan_approvals/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)  # New field to indicate approval status
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"{self.Applicant_first_name} {self.Applicant_last_name}"



#investor details
class investorapplicationdb(models.Model):
    Investor_first_name = models.CharField(max_length=100,default='')
    Investor_last_name = models.CharField(max_length=100,default='')
    Investor_email = models.EmailField(default='')
    Nominee_first_name = models.CharField(max_length=100,default='')
    Nominee_last_name = models.CharField(max_length=100,default='')
    Investor_adress = models.TextField(default='')
    Investor_phone = models.CharField(max_length=15,default='')
    Nominee_phone = models.CharField(max_length=15,default='')
    Investor_photo = models.FileField(upload_to='documents/investor_photos/', max_length=100, blank=True, null=True)
    Investor_pan = models.FileField(upload_to='documents/investor_pans/', max_length=100, blank=True, null=True)
    Investor_adhaar = models.FileField(upload_to='documents/investor_aadhaars/', max_length=100, blank=True, null=True)
    Investor_bank_statement = models.FileField(upload_to='documents/investor_bank_statements/', max_length=100, blank=True, null=True)
    Investor_bank_pass = models.FileField(upload_to='documents/investor_bank_passbooks/', max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    def __str__(self):
        return self.Investor_email

class InvestorOffer(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investor_offers')
    applicant = models.ForeignKey(loanapplicationdb, on_delete=models.CASCADE, related_name='applicant_offers')
    offer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    repayment_duration = models.PositiveIntegerField()  # duration in months
    offer_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Offer by {self.investor.username} to {self.applicant.Applicant_first_name}"

class Offer(models.Model):
    applicant = models.ForeignKey(loanapplicationdb, on_delete=models.CASCADE)
    investor = models.ForeignKey(investorapplicationdb, on_delete=models.CASCADE)
    offer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.IntegerField()  # Duration in months
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Choose this option

    def __str__(self):
        return f"Offer {self.offer_amount} by {self.investor.Investor_first_name} to {self.applicant}"

class LoanRepayment(models.Model):
    applicant = models.ForeignKey(loanapplicationdb, on_delete=models.CASCADE)
    investor = models.ForeignKey(investorapplicationdb, on_delete=models.CASCADE)
    offer_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Principal amount
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Annual interest rate in percentage
    total_repayment_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total amount including interest
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2)  # EMI amount
    total_installments = models.IntegerField()  # Total number of installments (months)
    installments_paid = models.IntegerField(default=0)  # Track how many installments are paid
    next_due_date = models.DateField()  # The next due date for installment
    repayment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])

    def __str__(self):
        return f"Repayment by {self.applicant.Applicant_email} to Investor ID {self.investor.id}"