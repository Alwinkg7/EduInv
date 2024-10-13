from django import forms
from EduInvApp.models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['offer_amount', 'interest_rate', 'duration']

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation logic if needed
        return cleaned_data

class InstallmentPaymentForm(forms.Form):
    installment_amount = forms.DecimalField(label='Installment Amount', max_digits=10, decimal_places=2)