from django import forms

class TransferForm(forms.Form):
    to_address = forms.CharField(label='Recipient Address', max_length=42)
    amount = forms.DecimalField(label='Amount', max_digits=18, decimal_places=8)