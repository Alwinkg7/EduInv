from EduInvApp import views
from django.urls import path
from .views import submit_offer  # Adjust import according to your views
from .views import client_details, accept_offer, reject_offer


urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('aboutpage/', views.aboutpage, name='aboutpage'),
    path('contactpage/', views.contactpage, name='contactpage'),
    path('clientsignuppage/', views.clientsignuppage, name='clientsignuppage'),
    path('investorsignuppage/', views.investorsignuppage, name='investorsignuppage'),
    path('userlogoutpageclient/', views.userlogoutpageclient, name='userlogoutpageclient'),
    path('userlogoutpageinvestor/', views.userlogoutpageinvestor, name='userlogoutpageinvestor'),
    path('clientpage/', views.clientpage, name='clientpage'),
    path('investorpage/', views.investorpage, name='investorpage'),
    path('applyforloanpage/', views.applyforloanpage, name='applyforloanpage'),
    path('investnowpage/', views.investnowpage, name='investnowpage'),
    path('savedatasignuppageclient/', views.savedatasignuppageclient, name='savedatasignuppageclient'),
    path('savedatasignuppageinvestor/', views.savedatasignuppageinvestor, name='savedatasignuppageinvestor'),
    path('savedatacontact/', views.savedatacontact, name='savedatacontact'),
    path('userloginpageclient/', views.userloginpageclient, name='userloginpageclient'),
    path('userloginpageinvestor/', views.userloginpageinvestor, name='userloginpageinvestor'),
    path('saveinvestorapplication/', views.saveinvestorapplication, name='saveinvestorapplication'),
    path('investor-login/', views.investor_login, name='investor_login'),
    path('investor_dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('submit-offer/<int:applicant_id>/', submit_offer, name='submit_offer'),
    path('saveapplicantloan/', views.saveapplicantloan, name='saveapplicantloan'),
    path('applicant/<int:applicant_id>/', views.applicant_details, name='applicant_details'),
    path('client/<int:client_id>/', views.client_details, name='client_details'),
    path('applicant_dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('accept_offer/<int:offer_id>/', views.accept_offer, name='accept_offer'),
    path('reject_offer/<int:offer_id>/', views.reject_offer, name='reject_offer'),
    path('applicant/login/', views.applicant_login, name='applicant_login'),
    path('applicant_login/', views.applicant_login, name='applicant_login'),
    path('investor_login/', views.investor_login, name='investor_login'),
    path('payment_gateway/<int:offer_id>/', views.payment_gateway, name='payment_gateway'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('top-investors/', views.top_investors, name='top_investors'),
    path('loan-repayment/<int:loan_id>/', views.loan_repayment, name='loan_repayment'),
    path('repayment-success/', views.repayment_success, name='repayment_success'),
]


