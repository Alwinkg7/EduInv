from AdminApp import views
from django.urls import path
urlpatterns = [
    path('Adminpanelpage/', views.Adminpanelpage, name='Adminpanelpage'),
    path('Adminloginpage/', views.Adminloginpage, name='Adminloginpage'),
    path('Adminlogin/', views.Adminlogin, name='Adminlogin'),
    path('clientspage/', views.clientspage, name='clientspage'),
    path('applicant/<int:applicant_id>/', views.applicantdetails, name='applicantdetails'),
    path('investor/<int:investor_id>/', views.investordetails, name='investordetails'),
    path('investorspage/', views.investorspage, name='investorspage'),
    path('investordetailspage/', views.investordetailspage, name='investordetailspage'),
    path('loanapplicationspage/', views.loanapplicationspage, name='loanapplicationspage'),
    path('displayclientsignup/', views.displayclientsignup, name='displayclientsignup'),
    path('displayinvestorsignup/', views.displayinvestorsignup, name='displayinvestorsignup'),
    path('displaycontact/', views.displaycontact, name='displaycontact'),
    path('displayinvestordetails/', views.displayinvestordetails, name='displayinvestordetails'),
    path('displayloanapplications/', views.displayloanapplications, name='displayloanapplications'),
    path('deleteloandata/<int:dataid>/', views.deleteloandata, name='deleteloandata'),
    path('deleteinvestdata/<int:dataid>/', views.deleteinvestdata, name='deleteinvestdata'),
    path('deleteclientdata/<int:dataid>/', views.deleteclientdata, name='deleteclientdata'),
    path('deleteinvestordata/<int:dataid>/', views.deleteinvestordata, name='deleteinvestordata'),
    path('approve_applicant/<int:applicant_id>/', views.approve_applicant, name='approve_applicant'),
    path('approve_investor/<int:investor_id>/', views.approve_investor, name='approve_investor'),
]